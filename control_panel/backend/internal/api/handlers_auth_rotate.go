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

func (h *authHandlers) rotateChallenge(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if h.checkAuthSourceLocked(c) || !h.allowChallengeCreation(c) {
		return
	}
	claims, ok := auth.ClaimsFrom(c)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	var req struct {
		NewPublicKeyPEM string `json:"new_public_key_pem"`
	}
	if !bindAuthJSON(c, &req) {
		return
	}
	admin, err := h.store.GetAdminByUsername(c, claims.Username)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	if admin.AuthState != db.AuthStateKeyActive || admin.AuthVersion != claims.AuthVersion || admin.PublicKeyPEM == nil || admin.PublicKeyFingerprint == nil {
		c.JSON(http.StatusConflict, gin.H{"error": "authentication state changed"})
		return
	}
	_, currentCanonicalPEM, currentFingerprint, err := auth.CanonicalizeP256PublicKeyPEM(*admin.PublicKeyPEM)
	if err != nil || currentCanonicalPEM != *admin.PublicKeyPEM || currentFingerprint != *admin.PublicKeyFingerprint {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "stored login key is invalid"})
		return
	}
	_, newCanonicalPEM, newFingerprint, err := auth.CanonicalizeP256PublicKeyPEM(req.NewPublicKeyPEM)
	if err != nil || newCanonicalPEM != req.NewPublicKeyPEM {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid P-256 public key"})
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
		Purpose:           db.AuthChallengeKeyRotate,
		AuthVersion:       claims.AuthVersion,
		KeyFingerprint:    currentFingerprint,
		NewKeyFingerprint: newFingerprint,
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
		"auth_version":        claims.AuthVersion,
		"key_fingerprint":     currentFingerprint,
		"new_key_fingerprint": newFingerprint,
		"expires_at":          challenge.ExpiresAt,
	})
}

func (h *authHandlers) rotateKey(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	if h.checkAuthSourceLocked(c) {
		return
	}
	claims, ok := auth.ClaimsFrom(c)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	var req struct {
		ChallengeID      string `json:"challenge_id"`
		NewPublicKeyPEM  string `json:"new_public_key_pem"`
		CurrentSignature string `json:"current_signature"`
		ProofSignature   string `json:"proof_signature"`
	}
	if !bindAuthJSON(c, &req) {
		return
	}
	challenge, err := h.store.ConsumeAuthChallenge(c, req.ChallengeID, db.AuthChallengeKeyRotate, time.Now().UTC())
	if err != nil {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	admin, err := h.store.GetAdminByUsername(c, claims.Username)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	if admin.AuthState != db.AuthStateKeyActive || admin.AuthVersion != challenge.AuthVersion || claims.AuthVersion != challenge.AuthVersion || admin.PublicKeyPEM == nil || admin.PublicKeyFingerprint == nil || *admin.PublicKeyFingerprint != challenge.KeyFingerprint {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	currentKey, currentCanonicalPEM, currentFingerprint, err := auth.CanonicalizeP256PublicKeyPEM(*admin.PublicKeyPEM)
	if err != nil || currentCanonicalPEM != *admin.PublicKeyPEM || currentFingerprint != challenge.KeyFingerprint {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	newKey, newCanonicalPEM, newFingerprint, err := auth.CanonicalizeP256PublicKeyPEM(req.NewPublicKeyPEM)
	if err != nil || newCanonicalPEM != req.NewPublicKeyPEM || newFingerprint != challenge.NewKeyFingerprint {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	proofContext := auth.ChallengeContext{
		ID: challenge.ChallengeID, Nonce: challenge.Nonce, Purpose: auth.PurposeKeyRotate,
		AuthVersion: challenge.AuthVersion, KeyFingerprint: challenge.KeyFingerprint,
		NewKeyFingerprint: challenge.NewKeyFingerprint,
	}
	currentMessage, err := auth.BuildChallengeMessage(proofContext, auth.ProofKeyRotate)
	if err != nil {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	currentDigest := sha256.Sum256(currentMessage)
	currentSignature, err := auth.DecodeCanonicalRawSignature(req.CurrentSignature)
	if err != nil || !auth.VerifyP256DigestSignature(currentKey, currentDigest[:], currentSignature) {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	newMessage, err := auth.BuildChallengeMessage(proofContext, auth.ProofNewKey)
	if err != nil {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	newDigest := sha256.Sum256(newMessage)
	newSignature, err := auth.DecodeCanonicalRawSignature(req.ProofSignature)
	if err != nil || !auth.VerifyP256DigestSignature(newKey, newDigest[:], newSignature) {
		h.rejectAuthAttempt(c, "auth.key_rotate", "failed")
		return
	}
	newVersion, err := h.store.RotateAdminKey(c, challenge.AuthVersion, challenge.KeyFingerprint, newCanonicalPEM, newFingerprint)
	if err != nil {
		if errors.Is(err, db.ErrAuthStateConflict) {
			c.JSON(http.StatusConflict, gin.H{"error": "authentication state changed; restart key rotation"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not rotate login key"})
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
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: admin.Username, Action: "auth.key_rotate", Result: "success"})
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}
