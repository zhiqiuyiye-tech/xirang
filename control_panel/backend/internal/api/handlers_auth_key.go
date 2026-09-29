package api

import (
	"crypto/sha256"
	"errors"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

func (h *authHandlers) bootstrapChallenge(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if !h.allowChallengeCreation(c) {
		return
	}
	var req struct {
		PublicKeyPEM string `json:"public_key_pem"`
	}
	if !bindAuthJSON(c, &req) {
		return
	}
	_, _, fingerprint, err := auth.CanonicalizeP256PublicKeyPEM(req.PublicKeyPEM)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid P-256 public key"})
		return
	}
	admin, err := h.store.GetAdminByUsername(c, "admin")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "authentication unavailable"})
		return
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap || admin.PublicKeyPEM != nil || admin.PublicKeyFingerprint != nil {
		c.JSON(http.StatusConflict, gin.H{"error": "key bootstrap is unavailable"})
		return
	}
	challengeID, err := generateRandomBase64URL(16)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	nonce, err := generateRandomBase64URL(32)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	now := time.Now().UTC()
	challenge := db.AuthChallenge{
		ChallengeID:       challengeID,
		Nonce:             nonce,
		Purpose:           db.AuthChallengeBootstrap,
		AuthVersion:       admin.AuthVersion,
		NewKeyFingerprint: fingerprint,
		ClientIP:          c.ClientIP(),
		CreatedAt:         now,
		ExpiresAt:         now.Add(2 * time.Minute),
	}
	if err := h.store.CreateAuthChallenge(c, challenge, h.challengeMaxPendingPerIP, h.challengeMaxPendingGlobal); err != nil {
		if errors.Is(err, db.ErrChallengeLimitExceeded) {
			c.Header("Retry-After", "60")
			c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many pending authentication challenges"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"challenge_id":        challengeID,
		"nonce":               nonce,
		"purpose":             challenge.Purpose,
		"auth_version":        admin.AuthVersion,
		"new_key_fingerprint": fingerprint,
		"expires_at":          challenge.ExpiresAt,
	})
}

func (h *authHandlers) bootstrap(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if h.checkAuthSourceLocked(c) {
		return
	}
	var req struct {
		Password       string `json:"password"`
		PublicKeyPEM   string `json:"public_key_pem"`
		ChallengeID    string `json:"challenge_id"`
		ProofSignature string `json:"proof_signature"`
	}
	if !bindAuthJSON(c, &req) {
		return
	}
	challenge, err := h.store.ConsumeAuthChallenge(c, req.ChallengeID, db.AuthChallengeBootstrap, time.Now().UTC())
	if err != nil {
		h.rejectAuthAttempt(c, "auth.bootstrap", "failed")
		return
	}
	admin, err := h.store.GetAdminByUsername(c, "admin")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "authentication unavailable"})
		return
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap || admin.AuthVersion != challenge.AuthVersion || admin.PublicKeyPEM != nil || admin.PublicKeyFingerprint != nil || !auth.CheckPassword(admin.PasswordHash, req.Password) {
		h.rejectAuthAttempt(c, "auth.bootstrap", "failed")
		return
	}
	publicKey, canonicalPEM, fingerprint, err := auth.CanonicalizeP256PublicKeyPEM(req.PublicKeyPEM)
	if err != nil || canonicalPEM != req.PublicKeyPEM || fingerprint != challenge.NewKeyFingerprint {
		h.rejectAuthAttempt(c, "auth.bootstrap", "failed")
		return
	}
	proofContext := auth.ChallengeContext{
		ID: challenge.ChallengeID, Nonce: challenge.Nonce, Purpose: auth.PurposeBootstrap,
		AuthVersion: challenge.AuthVersion, NewKeyFingerprint: challenge.NewKeyFingerprint,
	}
	message, err := auth.BuildChallengeMessage(proofContext, auth.ProofBootstrap)
	if err != nil {
		h.rejectAuthAttempt(c, "auth.bootstrap", "failed")
		return
	}
	digest := sha256.Sum256(message)
	signature, err := auth.DecodeCanonicalRawSignature(req.ProofSignature)
	if err != nil || !auth.VerifyP256DigestSignature(publicKey, digest[:], signature) {
		h.rejectAuthAttempt(c, "auth.bootstrap", "failed")
		return
	}
	newVersion, err := h.store.BootstrapAdminKey(c, challenge.AuthVersion, canonicalPEM, fingerprint)
	if err != nil {
		if errors.Is(err, db.ErrAuthStateConflict) {
			c.JSON(http.StatusConflict, gin.H{"error": "authentication state changed; restart bootstrap"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not register login key"})
		return
	}
	token, err := h.tk.Issue(admin.ID, admin.Username, newVersion)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not issue session"})
		return
	}
	if err := h.setSessionCookies(c, token); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create session cookies"})
		return
	}
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: admin.Username, Action: "auth.bootstrap", Result: "success"})
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

func (h *authHandlers) loginChallenge(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if !h.allowChallengeCreation(c) {
		return
	}
	admin, err := h.store.GetAdminByUsername(c, "admin")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "authentication unavailable"})
		return
	}
	if admin.AuthState != db.AuthStateKeyActive || admin.PublicKeyPEM == nil || admin.PublicKeyFingerprint == nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "key login is not configured"})
		return
	}
	challengeID, err := generateRandomBase64URL(16)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	nonce, err := generateRandomBase64URL(32)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	now := time.Now().UTC()
	challenge := db.AuthChallenge{
		ChallengeID:    challengeID,
		Nonce:          nonce,
		Purpose:        db.AuthChallengeLogin,
		AuthVersion:    admin.AuthVersion,
		KeyFingerprint: *admin.PublicKeyFingerprint,
		ClientIP:       c.ClientIP(),
		CreatedAt:      now,
		ExpiresAt:      now.Add(2 * time.Minute),
	}
	if err := h.store.CreateAuthChallenge(c, challenge, h.challengeMaxPendingPerIP, h.challengeMaxPendingGlobal); err != nil {
		if errors.Is(err, db.ErrChallengeLimitExceeded) {
			c.Header("Retry-After", "60")
			c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many pending authentication challenges"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create challenge"})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"challenge_id":    challengeID,
		"nonce":           nonce,
		"purpose":         challenge.Purpose,
		"auth_version":    challenge.AuthVersion,
		"key_fingerprint": challenge.KeyFingerprint,
		"expires_at":      challenge.ExpiresAt,
	})
}

func (h *authHandlers) login(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if h.checkAuthSourceLocked(c) {
		return
	}
	var req struct {
		ChallengeID string `json:"challenge_id"`
		Signature   string `json:"signature"`
	}
	if !bindAuthJSON(c, &req) {
		return
	}
	challenge, err := h.store.ConsumeAuthChallenge(c, req.ChallengeID, db.AuthChallengeLogin, time.Now().UTC())
	if err != nil {
		h.rejectAuthAttempt(c, "auth.login", "failed")
		return
	}
	admin, err := h.store.GetAdminByUsername(c, "admin")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "authentication unavailable"})
		return
	}
	if admin.AuthState != db.AuthStateKeyActive || admin.AuthVersion != challenge.AuthVersion || admin.PublicKeyPEM == nil || admin.PublicKeyFingerprint == nil || *admin.PublicKeyFingerprint != challenge.KeyFingerprint {
		h.rejectAuthAttempt(c, "auth.login", "failed")
		return
	}
	publicKey, canonicalPEM, fingerprint, err := auth.CanonicalizeP256PublicKeyPEM(*admin.PublicKeyPEM)
	if err != nil || canonicalPEM != *admin.PublicKeyPEM || fingerprint != challenge.KeyFingerprint {
		h.rejectAuthAttempt(c, "auth.login", "failed")
		return
	}
	proofContext := auth.ChallengeContext{
		ID: challenge.ChallengeID, Nonce: challenge.Nonce, Purpose: auth.PurposeLogin,
		AuthVersion: challenge.AuthVersion, KeyFingerprint: challenge.KeyFingerprint,
	}
	message, err := auth.BuildChallengeMessage(proofContext, auth.ProofLogin)
	if err != nil {
		h.rejectAuthAttempt(c, "auth.login", "failed")
		return
	}
	digest := sha256.Sum256(message)
	signature, err := auth.DecodeCanonicalRawSignature(req.Signature)
	if err != nil || !auth.VerifyP256DigestSignature(publicKey, digest[:], signature) {
		h.rejectAuthAttempt(c, "auth.login", "failed")
		return
	}
	token, err := h.tk.Issue(admin.ID, admin.Username, challenge.AuthVersion)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not issue session"})
		return
	}
	if err := h.setSessionCookies(c, token); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create session cookies"})
		return
	}
	if h.limiter != nil {
		h.limiter.RecordSuccess("auth:" + c.ClientIP())
	}
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: admin.Username, Action: "auth.login", Result: "success"})
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}
