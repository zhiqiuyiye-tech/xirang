package api

import (
	"bytes"
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"encoding/pem"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

func setupKeyAuthHandler(t *testing.T) (*db.Store, *auth.Tokens, *auth.RateLimiter, *authHandlers) {
	t.Helper()
	gin.SetMode(gin.TestMode)
	store, err := db.Open(filepath.Join(t.TempDir(), "key_auth_test.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	passwordHash, err := auth.HashPassword("initial-bootstrap-password")
	if err != nil {
		t.Fatal(err)
	}
	if err := store.UpsertAdminPassword(context.Background(), "admin", passwordHash); err != nil {
		t.Fatal(err)
	}
	tokens := auth.NewTokens("test-jwt-secret-key-32bytes-long", time.Minute*30)
	limiter := auth.NewRateLimiter(5, time.Minute, 15*time.Minute)
	t.Cleanup(limiter.Close)
	handler := newAuthHandlers(AuthHandlerConfig{
		Store:          store,
		Tokens:         tokens,
		Limiter:        limiter,
		CookieName:     "cp_session",
		CookieSecure:   false,
		CookieSameSite: "Strict",
		CSRFCookieName: "cp_csrf",
		TokenTTL:       time.Minute * 30,
	})
	return store, tokens, limiter, handler
}

func TestFailedBootstrapProofFromOneIPDoesNotLockAnotherSource(t *testing.T) {
	store, _, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	if err := configureTrustedProxies(router, nil); err != nil {
		t.Fatal(err)
	}
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)
	privateKey, publicKeyPEM, fingerprint := newP256AuthTestKey(t)

	for attempt := 0; attempt < 5; attempt++ {
		challengeBody, _ := json.Marshal(map[string]string{"public_key_pem": publicKeyPEM})
		challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(challengeBody))
		challengeRequest.RemoteAddr = "192.0.2.10:1234"
		challengeRequest.Header.Set("Content-Type", "application/json")
		challengeResponse := httptest.NewRecorder()
		router.ServeHTTP(challengeResponse, challengeRequest)
		if challengeResponse.Code != http.StatusOK {
			t.Fatalf("source A challenge %d status=%d body=%s", attempt, challengeResponse.Code, challengeResponse.Body.String())
		}
		var challenge struct {
			ID string `json:"challenge_id"`
		}
		if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
			t.Fatal(err)
		}
		badBody, _ := json.Marshal(map[string]string{
			"password": "initial-bootstrap-password", "public_key_pem": publicKeyPEM,
			"challenge_id": challenge.ID, "proof_signature": strings.Repeat("A", 86),
		})
		request := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(badBody))
		request.RemoteAddr = "192.0.2.10:1234"
		request.Header.Set("Content-Type", "application/json")
		response := httptest.NewRecorder()
		router.ServeHTTP(response, request)
		if attempt < 4 && response.Code != http.StatusUnauthorized {
			t.Fatalf("source A failure %d status=%d body=%s", attempt, response.Code, response.Body.String())
		}
		if attempt == 4 && response.Code != http.StatusTooManyRequests {
			t.Fatalf("source A lock status=%d body=%s", response.Code, response.Body.String())
		}
	}

	challengeBody, _ := json.Marshal(map[string]string{"public_key_pem": publicKeyPEM})
	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(challengeBody))
	challengeRequest.RemoteAddr = "198.51.100.20:4321"
	challengeRequest.Header.Set("Content-Type", "application/json")
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("source B challenge blocked by source A: status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID          string `json:"challenge_id"`
		Nonce       string `json:"nonce"`
		AuthVersion int64  `json:"auth_version"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	proofContext := auth.ChallengeContext{ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeBootstrap, AuthVersion: challenge.AuthVersion, NewKeyFingerprint: fingerprint}
	proof := signChallengeForTest(t, privateKey, proofContext, auth.ProofBootstrap)
	validBody, _ := json.Marshal(map[string]string{
		"password": "initial-bootstrap-password", "public_key_pem": publicKeyPEM,
		"challenge_id": challenge.ID, "proof_signature": proof,
	})
	validRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(validBody))
	validRequest.RemoteAddr = "198.51.100.20:4321"
	validRequest.Header.Set("Content-Type", "application/json")
	validResponse := httptest.NewRecorder()
	router.ServeHTTP(validResponse, validRequest)
	if validResponse.Code != http.StatusOK {
		t.Fatalf("source B bootstrap blocked by source A: status=%d body=%s", validResponse.Code, validResponse.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != db.AuthStateKeyActive {
		t.Fatalf("source B did not complete bootstrap: %+v", admin)
	}
}

func TestBootstrapRejectsOversizedRequestBody(t *testing.T) {
	store, _, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	body := []byte(`{"public_key_pem":"` + strings.Repeat("A", 9*1024) + `"}`)
	request := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(body))
	request.Header.Set("Content-Type", "application/json")
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)
	if response.Code != http.StatusBadRequest {
		t.Fatalf("oversized request status=%d body=%s", response.Code, response.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap {
		t.Fatalf("oversized request changed auth state to %s", admin.AuthState)
	}
}

func TestAuthStatusReportsPasswordBootstrap(t *testing.T) {
	_, _, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	router.GET("/api/v1/auth/status", handler.status)
	request := httptest.NewRequest(http.MethodGet, "/api/v1/auth/status", nil)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)
	if response.Code != http.StatusOK {
		t.Fatalf("status = %d body=%s", response.Code, response.Body.String())
	}
	var result struct {
		AuthState   string  `json:"auth_state"`
		Fingerprint *string `json:"key_fingerprint"`
	}
	if err := json.Unmarshal(response.Body.Bytes(), &result); err != nil {
		t.Fatal(err)
	}
	if result.AuthState != string(db.AuthStatePasswordBootstrap) || result.Fingerprint != nil {
		t.Fatalf("unexpected auth status: %+v", result)
	}
	if response.Header().Get("Cache-Control") != "no-store" {
		t.Fatal("auth status response must be no-store")
	}
}

func newP256AuthTestKey(t *testing.T) (*ecdsa.PrivateKey, string, string) {
	t.Helper()
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	der, err := x509.MarshalPKIXPublicKey(&privateKey.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	input := string(pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: der}))
	_, canonicalPEM, fingerprint, err := auth.CanonicalizeP256PublicKeyPEM(input)
	if err != nil {
		t.Fatal(err)
	}
	return privateKey, canonicalPEM, fingerprint
}

func signChallengeForTest(t *testing.T, privateKey *ecdsa.PrivateKey, challenge auth.ChallengeContext, proof auth.ProofKind) string {
	t.Helper()
	message, err := auth.BuildChallengeMessage(challenge, proof)
	if err != nil {
		t.Fatal(err)
	}
	digest := sha256.Sum256(message)
	r, s, err := ecdsa.Sign(rand.Reader, privateKey, digest[:])
	if err != nil {
		t.Fatal(err)
	}
	raw := make([]byte, 64)
	r.FillBytes(raw[:32])
	s.FillBytes(raw[32:])
	return base64.RawURLEncoding.EncodeToString(raw)
}

func TestBootstrapRegistersOnlyProvenPrivateKey(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)
	router.POST("/api/v1/auth/login", handler.login)

	privateKey, publicKeyPEM, fingerprint := newP256AuthTestKey(t)
	adminBefore, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	challengeBody, _ := json.Marshal(map[string]string{"public_key_pem": publicKeyPEM})
	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(challengeBody))
	challengeRequest.Header.Set("Content-Type", "application/json")
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("bootstrap challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID             string `json:"challenge_id"`
		Nonce          string `json:"nonce"`
		AuthVersion    int64  `json:"auth_version"`
		NewFingerprint string `json:"new_key_fingerprint"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	if len(challenge.ID) != 22 || len(challenge.Nonce) != 43 || challenge.AuthVersion != adminBefore.AuthVersion || challenge.NewFingerprint != fingerprint {
		t.Fatalf("unexpected bootstrap challenge: %+v", challenge)
	}
	challengeContext := auth.ChallengeContext{
		ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeBootstrap,
		AuthVersion: challenge.AuthVersion, NewKeyFingerprint: challenge.NewFingerprint,
	}
	proof := signChallengeForTest(t, privateKey, challengeContext, auth.ProofBootstrap)
	bootstrapBody, _ := json.Marshal(map[string]string{
		"password": "initial-bootstrap-password", "public_key_pem": publicKeyPEM,
		"challenge_id": challenge.ID, "proof_signature": proof,
	})
	bootstrapRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(bootstrapBody))
	bootstrapRequest.Header.Set("Content-Type", "application/json")
	bootstrapResponse := httptest.NewRecorder()
	router.ServeHTTP(bootstrapResponse, bootstrapRequest)
	if bootstrapResponse.Code != http.StatusOK {
		t.Fatalf("bootstrap status=%d body=%s", bootstrapResponse.Code, bootstrapResponse.Body.String())
	}
	if strings.Contains(bootstrapResponse.Body.String(), "token") || strings.Contains(bootstrapResponse.Body.String(), "csrf_token") {
		t.Fatalf("bootstrap JSON leaked session material: %s", bootstrapResponse.Body.String())
	}
	var sessionCookie *http.Cookie
	for _, cookie := range bootstrapResponse.Result().Cookies() {
		if cookie.Name == "cp_session" {
			sessionCookie = cookie
			if !cookie.HttpOnly || cookie.SameSite != http.SameSiteStrictMode {
				t.Fatalf("session cookie attributes: %+v", cookie)
			}
		}
	}
	if sessionCookie == nil {
		t.Fatal("bootstrap did not set an HttpOnly session cookie")
	}
	claims, err := tokens.Parse(sessionCookie.Value)
	if err != nil {
		t.Fatal(err)
	}
	adminAfter, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if claims.AuthVersion != adminAfter.AuthVersion || claims.AuthVersion != challenge.AuthVersion+1 {
		t.Fatalf("session auth_version=%d admin=%d challenge=%d", claims.AuthVersion, adminAfter.AuthVersion, challenge.AuthVersion)
	}
	if adminAfter.AuthState != db.AuthStateKeyActive || adminAfter.PasswordHash != "__DISABLED_AFTER_KEY_BOOTSTRAP__" {
		t.Fatalf("password bootstrap was not disabled: %+v", adminAfter)
	}
	passwordBody, _ := json.Marshal(map[string]string{"username": "admin", "password": "initial-bootstrap-password"})
	passwordRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(passwordBody))
	passwordRequest.Header.Set("Content-Type", "application/json")
	passwordResponse := httptest.NewRecorder()
	router.ServeHTTP(passwordResponse, passwordRequest)
	if passwordResponse.Code != http.StatusUnauthorized {
		t.Fatalf("password login after key enrollment status=%d", passwordResponse.Code)
	}
}

func TestBootstrapRejectsAndConsumesInvalidProof(t *testing.T) {
	store, _, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)
	privateKey, publicKeyPEM, fingerprint := newP256AuthTestKey(t)

	challengeBody, _ := json.Marshal(map[string]string{"public_key_pem": publicKeyPEM})
	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(challengeBody))
	challengeRequest.Header.Set("Content-Type", "application/json")
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("bootstrap challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID          string `json:"challenge_id"`
		Nonce       string `json:"nonce"`
		AuthVersion int64  `json:"auth_version"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	challengeContext := auth.ChallengeContext{
		ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeBootstrap,
		AuthVersion: challenge.AuthVersion, NewKeyFingerprint: fingerprint,
	}
	validProof := signChallengeForTest(t, privateKey, challengeContext, auth.ProofBootstrap)
	badProof := strings.Repeat("A", 86)
	body := map[string]string{
		"password": "initial-bootstrap-password", "public_key_pem": publicKeyPEM,
		"challenge_id": challenge.ID, "proof_signature": badProof,
	}
	encoded, _ := json.Marshal(body)
	request := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(encoded))
	request.Header.Set("Content-Type", "application/json")
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)
	if response.Code != http.StatusUnauthorized {
		t.Fatalf("invalid proof status=%d body=%s", response.Code, response.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap || admin.AuthVersion != challenge.AuthVersion {
		t.Fatalf("invalid proof changed auth state: %+v", admin)
	}

	body["proof_signature"] = validProof
	encoded, _ = json.Marshal(body)
	retry := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(encoded))
	retry.Header.Set("Content-Type", "application/json")
	retryResponse := httptest.NewRecorder()
	router.ServeHTTP(retryResponse, retry)
	if retryResponse.Code != http.StatusUnauthorized {
		t.Fatalf("replayed challenge status=%d body=%s", retryResponse.Code, retryResponse.Body.String())
	}
	admin, err = store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap || admin.AuthVersion != challenge.AuthVersion {
		t.Fatalf("replayed challenge changed auth state: %+v", admin)
	}
}

func registerTestKey(t *testing.T, store *db.Store, router *gin.Engine) (*ecdsa.PrivateKey, string, string, int64) {
	t.Helper()
	privateKey, publicKeyPEM, fingerprint := newP256AuthTestKey(t)
	challengeBody, _ := json.Marshal(map[string]string{"public_key_pem": publicKeyPEM})
	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", bytes.NewReader(challengeBody))
	challengeRequest.Header.Set("Content-Type", "application/json")
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("bootstrap challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID          string `json:"challenge_id"`
		Nonce       string `json:"nonce"`
		AuthVersion int64  `json:"auth_version"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	proofContext := auth.ChallengeContext{ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeBootstrap, AuthVersion: challenge.AuthVersion, NewKeyFingerprint: fingerprint}
	proof := signChallengeForTest(t, privateKey, proofContext, auth.ProofBootstrap)
	bootstrapBody, _ := json.Marshal(map[string]string{
		"password": "initial-bootstrap-password", "public_key_pem": publicKeyPEM,
		"challenge_id": challenge.ID, "proof_signature": proof,
	})
	bootstrapRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(bootstrapBody))
	bootstrapRequest.Header.Set("Content-Type", "application/json")
	bootstrapResponse := httptest.NewRecorder()
	router.ServeHTTP(bootstrapResponse, bootstrapRequest)
	if bootstrapResponse.Code != http.StatusOK {
		t.Fatalf("bootstrap status=%d body=%s", bootstrapResponse.Code, bootstrapResponse.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	return privateKey, publicKeyPEM, fingerprint, admin.AuthVersion
}

func TestLoginChallengeSignsSessionWithChallengeVersion(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	router := gin.New()
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)
	router.POST("/api/v1/auth/challenges/login", handler.loginChallenge)
	router.POST("/api/v1/auth/login", handler.login)
	privateKey, _, fingerprint, activeVersion := registerTestKey(t, store, router)

	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/login", nil)
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("login challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID          string `json:"challenge_id"`
		Nonce       string `json:"nonce"`
		AuthVersion int64  `json:"auth_version"`
		Fingerprint string `json:"key_fingerprint"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	if challenge.AuthVersion != activeVersion || challenge.Fingerprint != fingerprint {
		t.Fatalf("login challenge not bound to active key/version: %+v", challenge)
	}
	proofContext := auth.ChallengeContext{ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeLogin, AuthVersion: challenge.AuthVersion, KeyFingerprint: challenge.Fingerprint}
	signature := signChallengeForTest(t, privateKey, proofContext, auth.ProofLogin)
	loginBody, _ := json.Marshal(map[string]string{"challenge_id": challenge.ID, "signature": signature})
	loginRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(loginBody))
	loginRequest.Header.Set("Content-Type", "application/json")
	loginResponse := httptest.NewRecorder()
	router.ServeHTTP(loginResponse, loginRequest)
	if loginResponse.Code != http.StatusOK {
		t.Fatalf("login status=%d body=%s", loginResponse.Code, loginResponse.Body.String())
	}
	if strings.Contains(loginResponse.Body.String(), "token") || strings.Contains(loginResponse.Body.String(), "csrf_token") {
		t.Fatalf("login JSON exposed credential material: %s", loginResponse.Body.String())
	}
	var sessionCookie *http.Cookie
	for _, cookie := range loginResponse.Result().Cookies() {
		if cookie.Name == "cp_session" {
			sessionCookie = cookie
		}
	}
	if sessionCookie == nil {
		t.Fatal("login did not set the session cookie")
	}
	claims, err := tokens.Parse(sessionCookie.Value)
	if err != nil {
		t.Fatal(err)
	}
	if claims.AuthVersion != challenge.AuthVersion {
		t.Fatalf("session auth_version=%d, challenge auth_version=%d", claims.AuthVersion, challenge.AuthVersion)
	}

	replay := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(loginBody))
	replay.Header.Set("Content-Type", "application/json")
	replayResponse := httptest.NewRecorder()
	router.ServeHTTP(replayResponse, replay)
	if replayResponse.Code != http.StatusUnauthorized {
		t.Fatalf("replay status=%d body=%s", replayResponse.Code, replayResponse.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthVersion != activeVersion {
		t.Fatalf("failed challenge replay changed auth_version to %d", admin.AuthVersion)
	}
}

func keyAuthTestRouter(store *db.Store, tokens *auth.Tokens, handler *authHandlers) *gin.Engine {
	router := gin.New()
	if err := configureTrustedProxies(router, nil); err != nil {
		panic(err)
	}
	router.GET("/api/v1/auth/status", handler.status)
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)
	router.POST("/api/v1/auth/challenges/login", handler.loginChallenge)
	router.POST("/api/v1/auth/login", handler.login)
	authed := router.Group("")
	authed.Use(auth.AuthMiddleware(auth.MiddlewareConfig{Tokens: tokens, VersionStore: store, CookieName: "cp_session"}))
	authed.Use(auth.CSRFMiddleware(auth.CSRFConfig{CookieName: "cp_csrf", HeaderName: "X-CSRF-Token"}))
	authed.GET("/auth/me", handler.me)
	authed.POST("/api/v1/auth/challenges/rotate", handler.rotateChallenge)
	authed.PUT("/api/v1/auth/key", handler.rotateKey)
	return router
}

func authenticatedJSONRequest(method, path, token, csrf string, body []byte) *http.Request {
	request := httptest.NewRequest(method, path, bytes.NewReader(body))
	request.Header.Set("Content-Type", "application/json")
	request.AddCookie(&http.Cookie{Name: "cp_session", Value: token})
	request.AddCookie(&http.Cookie{Name: "cp_csrf", Value: csrf})
	request.Header.Set("X-CSRF-Token", csrf)
	return request
}

func TestRotationRequiresCurrentAndNewKeyProofs(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	router := keyAuthTestRouter(store, tokens, handler)
	currentPrivate, _, currentFingerprint, currentVersion := registerTestKey(t, store, router)
	newPrivate, newPublicPEM, newFingerprint := newP256AuthTestKey(t)
	session, err := tokens.Issue(1, "admin", currentVersion)
	if err != nil {
		t.Fatal(err)
	}

	challengeBody, _ := json.Marshal(map[string]string{"new_public_key_pem": newPublicPEM})
	challengeRequest := authenticatedJSONRequest(http.MethodPost, "/api/v1/auth/challenges/rotate", session, "csrf-value", challengeBody)
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("rotation challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID                string `json:"challenge_id"`
		Nonce             string `json:"nonce"`
		AuthVersion       int64  `json:"auth_version"`
		KeyFingerprint    string `json:"key_fingerprint"`
		NewKeyFingerprint string `json:"new_key_fingerprint"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	if challenge.AuthVersion != currentVersion || challenge.KeyFingerprint != currentFingerprint || challenge.NewKeyFingerprint != newFingerprint {
		t.Fatalf("rotation challenge binding mismatch: %+v", challenge)
	}
	proofContext := auth.ChallengeContext{
		ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeKeyRotate,
		AuthVersion: challenge.AuthVersion, KeyFingerprint: currentFingerprint, NewKeyFingerprint: newFingerprint,
	}
	currentProof := signChallengeForTest(t, currentPrivate, proofContext, auth.ProofKeyRotate)
	wrongNewProof := signChallengeForTest(t, currentPrivate, proofContext, auth.ProofNewKey)
	rotationBody, _ := json.Marshal(map[string]string{
		"challenge_id": challenge.ID, "new_public_key_pem": newPublicPEM,
		"current_signature": currentProof, "proof_signature": wrongNewProof,
	})
	rotationRequest := authenticatedJSONRequest(http.MethodPut, "/api/v1/auth/key", session, "csrf-value", rotationBody)
	rotationResponse := httptest.NewRecorder()
	router.ServeHTTP(rotationResponse, rotationRequest)
	if rotationResponse.Code != http.StatusUnauthorized {
		t.Fatalf("rotation without new-key PoP status=%d body=%s", rotationResponse.Code, rotationResponse.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthVersion != currentVersion || admin.PublicKeyFingerprint == nil || *admin.PublicKeyFingerprint != currentFingerprint {
		t.Fatalf("failed PoP changed active key: %+v", admin)
	}

	correctNewProof := signChallengeForTest(t, newPrivate, proofContext, auth.ProofNewKey)
	rotationBody, _ = json.Marshal(map[string]string{
		"challenge_id": challenge.ID, "new_public_key_pem": newPublicPEM,
		"current_signature": currentProof, "proof_signature": correctNewProof,
	})
	replayRequest := authenticatedJSONRequest(http.MethodPut, "/api/v1/auth/key", session, "csrf-value", rotationBody)
	replayResponse := httptest.NewRecorder()
	router.ServeHTTP(replayResponse, replayRequest)
	if replayResponse.Code != http.StatusUnauthorized {
		t.Fatalf("consumed rotation challenge replay status=%d", replayResponse.Code)
	}
	admin, err = store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthVersion != currentVersion {
		t.Fatalf("replayed rotation changed version to %d", admin.AuthVersion)
	}
}

func TestRotationSucceedsWithBothProofsAndCasVersion(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	router := keyAuthTestRouter(store, tokens, handler)
	currentPrivate, _, currentFingerprint, currentVersion := registerTestKey(t, store, router)
	newPrivate, newPublicPEM, newFingerprint := newP256AuthTestKey(t)
	oldSession, err := tokens.Issue(1, "admin", currentVersion)
	if err != nil {
		t.Fatal(err)
	}

	challengeBody, _ := json.Marshal(map[string]string{"new_public_key_pem": newPublicPEM})
	challengeRequest := authenticatedJSONRequest(http.MethodPost, "/api/v1/auth/challenges/rotate", oldSession, "csrf-value", challengeBody)
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("rotation challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID                string `json:"challenge_id"`
		Nonce             string `json:"nonce"`
		AuthVersion       int64  `json:"auth_version"`
		KeyFingerprint    string `json:"key_fingerprint"`
		NewKeyFingerprint string `json:"new_key_fingerprint"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	proofContext := auth.ChallengeContext{
		ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeKeyRotate,
		AuthVersion: challenge.AuthVersion, KeyFingerprint: currentFingerprint, NewKeyFingerprint: newFingerprint,
	}
	currentProof := signChallengeForTest(t, currentPrivate, proofContext, auth.ProofKeyRotate)
	newProof := signChallengeForTest(t, newPrivate, proofContext, auth.ProofNewKey)
	rotationBody, _ := json.Marshal(map[string]string{
		"challenge_id": challenge.ID, "new_public_key_pem": newPublicPEM,
		"current_signature": currentProof, "proof_signature": newProof,
	})
	rotationRequest := authenticatedJSONRequest(http.MethodPut, "/api/v1/auth/key", oldSession, "csrf-value", rotationBody)
	rotationResponse := httptest.NewRecorder()
	router.ServeHTTP(rotationResponse, rotationRequest)
	if rotationResponse.Code != http.StatusOK {
		t.Fatalf("rotation status=%d body=%s", rotationResponse.Code, rotationResponse.Body.String())
	}
	if strings.Contains(rotationResponse.Body.String(), "token") || strings.Contains(rotationResponse.Body.String(), "csrf_token") {
		t.Fatalf("rotation JSON exposed session material: %s", rotationResponse.Body.String())
	}
	var newSession *http.Cookie
	for _, cookie := range rotationResponse.Result().Cookies() {
		if cookie.Name == "cp_session" {
			newSession = cookie
		}
	}
	if newSession == nil {
		t.Fatal("rotation did not issue a replacement session")
	}
	claims, err := tokens.Parse(newSession.Value)
	if err != nil {
		t.Fatal(err)
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if claims.AuthVersion != currentVersion+1 || claims.AuthVersion != admin.AuthVersion || admin.PublicKeyFingerprint == nil || *admin.PublicKeyFingerprint != newFingerprint {
		t.Fatalf("rotation result mismatch: claims=%d admin=%+v", claims.AuthVersion, admin)
	}
	oldResponse := sendCookieAuthRequest(t, router, http.MethodGet, "/auth/me", oldSession)
	if oldResponse.Code != http.StatusUnauthorized {
		t.Fatalf("old session survived rotation: status=%d", oldResponse.Code)
	}
	newResponse := sendCookieAuthRequest(t, router, http.MethodGet, "/auth/me", newSession.Value)
	if newResponse.Code != http.StatusOK {
		t.Fatalf("new session rejected: status=%d body=%s", newResponse.Code, newResponse.Body.String())
	}
}

func TestRouterRegistersAuthStatusEndpoint(t *testing.T) {
	router, _, _, _ := newRouter(t)
	request := httptest.NewRequest(http.MethodGet, "/api/v1/auth/status", nil)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)
	if response.Code != http.StatusOK {
		t.Fatalf("GET /auth/status status=%d body=%s", response.Code, response.Body.String())
	}
	passwordRequest := httptest.NewRequest(http.MethodPut, "/api/v1/auth/password", nil)
	passwordResponse := httptest.NewRecorder()
	router.ServeHTTP(passwordResponse, passwordRequest)
	if passwordResponse.Code != http.StatusNotFound {
		t.Fatalf("legacy password endpoint status=%d, want 404", passwordResponse.Code)
	}
	logoutAllRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/logout-all", nil)
	logoutAllResponse := httptest.NewRecorder()
	router.ServeHTTP(logoutAllResponse, logoutAllRequest)
	if logoutAllResponse.Code != http.StatusUnauthorized {
		t.Fatalf("logout-all route status=%d, want authentication challenge 401", logoutAllResponse.Code)
	}
}

func setupLogoutAuthRouter(t *testing.T, store *db.Store, tokens *auth.Tokens, handler *authHandlers) *gin.Engine {
	t.Helper()
	router := gin.New()
	group := router.Group("")
	group.Use(auth.AuthMiddleware(auth.MiddlewareConfig{Tokens: tokens, VersionStore: store, CookieName: "cp_session"}))
	group.Use(auth.CSRFMiddleware(auth.CSRFConfig{CookieName: "cp_csrf", HeaderName: "X-CSRF-Token"}))
	group.POST("/auth/logout", handler.logout)
	group.POST("/auth/logout-all", handler.logoutAll)
	group.GET("/auth/me", handler.me)
	return router
}

func sendCookieAuthRequest(t *testing.T, router *gin.Engine, method, path, token string) *httptest.ResponseRecorder {
	t.Helper()
	request := httptest.NewRequest(method, path, nil)
	request.AddCookie(&http.Cookie{Name: "cp_session", Value: token})
	request.AddCookie(&http.Cookie{Name: "cp_csrf", Value: "csrf-value"})
	request.Header.Set("X-CSRF-Token", "csrf-value")
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)
	return response
}

func TestLogoutCurrentBrowserDoesNotRevokeSharedSessions(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	version, err := store.GetAdminAuthVersion(context.Background(), 1)
	if err != nil {
		t.Fatal(err)
	}
	currentBrowserToken, _ := tokens.Issue(1, "admin", version)
	otherBrowserToken, _ := tokens.Issue(1, "admin", version)
	router := setupLogoutAuthRouter(t, store, tokens, handler)

	response := sendCookieAuthRequest(t, router, http.MethodPost, "/auth/logout", currentBrowserToken)
	if response.Code != http.StatusOK {
		t.Fatalf("logout status=%d body=%s", response.Code, response.Body.String())
	}
	currentVersion, err := store.GetAdminAuthVersion(context.Background(), 1)
	if err != nil {
		t.Fatal(err)
	}
	if currentVersion != version {
		t.Fatalf("local logout changed auth_version from %d to %d", version, currentVersion)
	}
	otherResponse := sendCookieAuthRequest(t, router, http.MethodGet, "/auth/me", otherBrowserToken)
	if otherResponse.Code != http.StatusOK {
		t.Fatalf("other browser session was revoked: status=%d body=%s", otherResponse.Code, otherResponse.Body.String())
	}
}

func TestLogoutAllRevokesEverySharedSession(t *testing.T) {
	store, tokens, _, handler := setupKeyAuthHandler(t)
	version, err := store.GetAdminAuthVersion(context.Background(), 1)
	if err != nil {
		t.Fatal(err)
	}
	currentBrowserToken, _ := tokens.Issue(1, "admin", version)
	otherBrowserToken, _ := tokens.Issue(1, "admin", version)
	router := setupLogoutAuthRouter(t, store, tokens, handler)

	response := sendCookieAuthRequest(t, router, http.MethodPost, "/auth/logout-all", currentBrowserToken)
	if response.Code != http.StatusOK {
		t.Fatalf("logout-all status=%d body=%s", response.Code, response.Body.String())
	}
	currentVersion, err := store.GetAdminAuthVersion(context.Background(), 1)
	if err != nil {
		t.Fatal(err)
	}
	if currentVersion != version+1 {
		t.Fatalf("global logout auth_version=%d, want %d", currentVersion, version+1)
	}
	otherResponse := sendCookieAuthRequest(t, router, http.MethodGet, "/auth/me", otherBrowserToken)
	if otherResponse.Code != http.StatusUnauthorized {
		t.Fatalf("other browser survived global logout: status=%d", otherResponse.Code)
	}
}

func TestLoginRejectsChallengeAfterAuthVersionChanges(t *testing.T) {
	store, _, _, handler := setupKeyAuthHandler(t)
	router := keyAuthTestRouter(store, handler.tk, handler)
	privateKey, _, _, version := registerTestKey(t, store, router)
	challengeRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/login", nil)
	challengeRequest.RemoteAddr = "192.0.2.10:1234"
	challengeResponse := httptest.NewRecorder()
	router.ServeHTTP(challengeResponse, challengeRequest)
	if challengeResponse.Code != http.StatusOK {
		t.Fatalf("challenge status=%d body=%s", challengeResponse.Code, challengeResponse.Body.String())
	}
	var challenge struct {
		ID          string `json:"challenge_id"`
		Nonce       string `json:"nonce"`
		AuthVersion int64  `json:"auth_version"`
		Fingerprint string `json:"key_fingerprint"`
	}
	if err := json.Unmarshal(challengeResponse.Body.Bytes(), &challenge); err != nil {
		t.Fatal(err)
	}
	proofContext := auth.ChallengeContext{ID: challenge.ID, Nonce: challenge.Nonce, Purpose: auth.PurposeLogin, AuthVersion: challenge.AuthVersion, KeyFingerprint: challenge.Fingerprint}
	signature := signChallengeForTest(t, privateKey, proofContext, auth.ProofLogin)
	if _, err := store.RevokeAdminSessions(context.Background(), "admin"); err != nil {
		t.Fatal(err)
	}
	loginBody, _ := json.Marshal(map[string]string{"challenge_id": challenge.ID, "signature": signature})
	loginRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(loginBody))
	loginRequest.RemoteAddr = "192.0.2.10:1234"
	loginRequest.Header.Set("Content-Type", "application/json")
	loginResponse := httptest.NewRecorder()
	router.ServeHTTP(loginResponse, loginRequest)
	if loginResponse.Code != http.StatusUnauthorized {
		t.Fatalf("stale challenge login status=%d body=%s", loginResponse.Code, loginResponse.Body.String())
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthVersion != version+1 {
		t.Fatalf("failed stale challenge changed auth_version to %d", admin.AuthVersion)
	}
}

func TestUnauthenticatedFailureAuditsShareBoundedWriteBudget(t *testing.T) {
	// The audit budget permits 60 unauthenticated failure records per minute.
	const expectedAuditBudget = 60

	store, _, limiter, handler := setupKeyAuthHandler(t)
	handler.challengeRateLimitPerMinute = 1
	router := gin.New()
	if err := configureTrustedProxies(router, nil); err != nil {
		t.Fatal(err)
	}
	router.POST("/api/v1/auth/challenges/bootstrap", handler.bootstrapChallenge)
	router.POST("/api/v1/auth/bootstrap", handler.bootstrap)

	// A failed proof consumes one slot and includes sentinel credentials in
	// the request so the audit assertion also guards against recording secrets.
	proofBody, err := json.Marshal(map[string]string{
		"password": "audit-sentinel-password", "challenge_id": "missing-challenge",
		"proof_signature": "audit-sentinel-signature",
	})
	if err != nil {
		t.Fatal(err)
	}
	proofRequest := httptest.NewRequest(http.MethodPost, "/api/v1/auth/bootstrap", bytes.NewReader(proofBody))
	proofRequest.RemoteAddr = "192.0.2.10:1234"
	proofRequest.Header.Set("Content-Type", "application/json")
	proofResponse := httptest.NewRecorder()
	router.ServeHTTP(proofResponse, proofRequest)
	if proofResponse.Code != http.StatusUnauthorized {
		t.Fatalf("invalid bootstrap proof status=%d body=%s", proofResponse.Code, proofResponse.Body.String())
	}

	// Flood from distinct sources after independently exhausting each source's
	// challenge allowance. The shared budget must cap writes despite rotation.
	for i := 1; i <= expectedAuditBudget; i++ {
		ip := "198.18.0." + strconv.Itoa(i)
		if allowed, _ := limiter.AllowRequest("challenge:"+ip, 1, time.Minute); !allowed {
			t.Fatalf("could not pre-fill challenge allowance for source %s", ip)
		}
		request := httptest.NewRequest(http.MethodPost, "/api/v1/auth/challenges/bootstrap", nil)
		request.RemoteAddr = ip + ":1234"
		response := httptest.NewRecorder()
		router.ServeHTTP(response, request)
		if response.Code != http.StatusTooManyRequests {
			t.Fatalf("challenge limit for source %s status=%d body=%s", ip, response.Code, response.Body.String())
		}
	}

	audits, err := store.ListAudit(context.Background(), expectedAuditBudget+1)
	if err != nil {
		t.Fatal(err)
	}
	if len(audits) != expectedAuditBudget {
		t.Fatalf("unauthenticated failure audit rows=%d, want budget %d", len(audits), expectedAuditBudget)
	}
	proofAudits, challengeAudits := 0, 0
	for _, audit := range audits {
		switch audit.Action {
		case "auth.bootstrap":
			proofAudits++
		case "auth.challenge_rate_limited":
			challengeAudits++
		default:
			t.Fatalf("unexpected audit action from failure requests: %q", audit.Action)
		}
		if audit.ParamsJSON != nil || audit.Target != nil {
			t.Fatalf("failure audit must not contain request data: %+v", audit)
		}
	}
	if proofAudits != 1 || challengeAudits != expectedAuditBudget-1 {
		t.Fatalf("shared failure audit budget distribution: proof=%d challenge=%d", proofAudits, challengeAudits)
	}
}
