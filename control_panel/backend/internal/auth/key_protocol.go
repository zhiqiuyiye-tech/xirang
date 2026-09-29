package auth

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/pem"
	"errors"
	"fmt"
	"math/big"
	"strconv"
	"strings"
)

const (
	challengeIDBytes         = 16
	challengeNonceBytes      = 32
	rawP256SignatureBytes    = 64
	maxP256PublicKeyPEMBytes = 2048
)

type ChallengePurpose string

const (
	PurposeLogin     ChallengePurpose = "LOGIN"
	PurposeBootstrap ChallengePurpose = "BOOTSTRAP"
	PurposeKeyRotate ChallengePurpose = "KEY_ROTATE"
)

type ProofKind string

const (
	ProofLogin     ProofKind = "login"
	ProofBootstrap ProofKind = "bootstrap"
	ProofKeyRotate ProofKind = "key_rotate"
	ProofNewKey    ProofKind = "new_key"
)

type ChallengeContext struct {
	ID                string
	Nonce             string
	Purpose           ChallengePurpose
	AuthVersion       int64
	KeyFingerprint    string
	NewKeyFingerprint string
}

// CanonicalizeP256PublicKeyPEM parses a SubjectPublicKeyInfo PEM, requires
// ECDSA P-256, and returns canonical PEM plus the SHA-256 hex fingerprint of
// canonical DER.
func CanonicalizeP256PublicKeyPEM(pemText string) (*ecdsa.PublicKey, string, string, error) {
	if len(pemText) == 0 || len(pemText) > maxP256PublicKeyPEMBytes {
		return nil, "", "", errors.New("public key PEM has invalid size")
	}
	block, rest := pem.Decode([]byte(pemText))
	if block == nil || block.Type != "PUBLIC KEY" || len(strings.TrimSpace(string(rest))) != 0 {
		return nil, "", "", errors.New("invalid public key PEM")
	}
	parsed, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return nil, "", "", fmt.Errorf("parse public key: %w", err)
	}
	publicKey, ok := parsed.(*ecdsa.PublicKey)
	if !ok || publicKey.Curve != elliptic.P256() || publicKey.X == nil || publicKey.Y == nil || !publicKey.Curve.IsOnCurve(publicKey.X, publicKey.Y) {
		return nil, "", "", errors.New("public key must be ECDSA P-256")
	}
	der, err := x509.MarshalPKIXPublicKey(publicKey)
	if err != nil {
		return nil, "", "", fmt.Errorf("marshal canonical public key: %w", err)
	}
	fingerprint := sha256.Sum256(der)
	canonical := pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: der})
	return publicKey, string(canonical), hex.EncodeToString(fingerprint[:]), nil
}

// BuildChallengeMessage returns the exact UTF-8 bytes that a proof role signs.
func BuildChallengeMessage(challenge ChallengeContext, kind ProofKind) ([]byte, error) {
	if challenge.AuthVersion <= 0 {
		return nil, errors.New("challenge auth version must be positive")
	}
	if _, err := decodeCanonicalBase64URL(challenge.ID, challengeIDBytes); err != nil {
		return nil, fmt.Errorf("invalid challenge id: %w", err)
	}
	if _, err := decodeCanonicalBase64URL(challenge.Nonce, challengeNonceBytes); err != nil {
		return nil, fmt.Errorf("invalid challenge nonce: %w", err)
	}
	version := strconv.FormatInt(challenge.AuthVersion, 10)

	switch kind {
	case ProofLogin:
		if challenge.Purpose != PurposeLogin || !validFingerprint(challenge.KeyFingerprint) || challenge.NewKeyFingerprint != "" {
			return nil, errors.New("login proof does not match challenge")
		}
		return []byte(strings.Join([]string{
			"xirang-control-panel-login-v1",
			challenge.ID,
			challenge.Nonce,
			version,
			challenge.KeyFingerprint,
		}, "\n")), nil
	case ProofBootstrap:
		if challenge.Purpose != PurposeBootstrap || challenge.KeyFingerprint != "" || !validFingerprint(challenge.NewKeyFingerprint) {
			return nil, errors.New("bootstrap proof does not match challenge")
		}
		return []byte(strings.Join([]string{
			"xirang-control-panel-bootstrap-v1",
			challenge.ID,
			challenge.Nonce,
			version,
			challenge.NewKeyFingerprint,
		}, "\n")), nil
	case ProofKeyRotate:
		if challenge.Purpose != PurposeKeyRotate || !validFingerprint(challenge.KeyFingerprint) || !validFingerprint(challenge.NewKeyFingerprint) {
			return nil, errors.New("key rotation proof does not match challenge")
		}
		return []byte(strings.Join([]string{
			"xirang-control-panel-key-rotate-v1",
			challenge.ID,
			challenge.Nonce,
			version,
			challenge.KeyFingerprint,
			challenge.NewKeyFingerprint,
		}, "\n")), nil
	case ProofNewKey:
		if challenge.Purpose != PurposeKeyRotate || !validFingerprint(challenge.KeyFingerprint) || !validFingerprint(challenge.NewKeyFingerprint) {
			return nil, errors.New("new key proof does not match challenge")
		}
		return []byte(strings.Join([]string{
			"xirang-control-panel-new-key-proof-v1",
			challenge.ID,
			challenge.Nonce,
			version,
			challenge.NewKeyFingerprint,
		}, "\n")), nil
	default:
		return nil, errors.New("unknown proof kind")
	}
}

// DecodeCanonicalRawSignature accepts only a 64-byte, unpadded canonical
// base64url representation of the fixed-width r||s P-256 signature.
func DecodeCanonicalRawSignature(encoded string) ([rawP256SignatureBytes]byte, error) {
	var signature [rawP256SignatureBytes]byte
	if len(encoded) != 86 {
		return signature, errors.New("signature must be 86 base64url characters")
	}
	decoded, err := base64.RawURLEncoding.DecodeString(encoded)
	if err != nil || len(decoded) != rawP256SignatureBytes || base64.RawURLEncoding.EncodeToString(decoded) != encoded {
		return signature, errors.New("signature is not canonical base64url")
	}
	copy(signature[:], decoded)
	return signature, nil
}

// VerifyP256DigestSignature verifies a 32-byte SHA-256 digest and fixed-width
// r||s P-256 signature.
func VerifyP256DigestSignature(publicKey *ecdsa.PublicKey, digest []byte, signature [rawP256SignatureBytes]byte) bool {
	if publicKey == nil || publicKey.Curve != elliptic.P256() || len(digest) != sha256.Size {
		return false
	}
	r := new(big.Int).SetBytes(signature[:32])
	s := new(big.Int).SetBytes(signature[32:])
	order := publicKey.Curve.Params().N
	if r.Sign() <= 0 || s.Sign() <= 0 || r.Cmp(order) >= 0 || s.Cmp(order) >= 0 {
		return false
	}
	return ecdsa.Verify(publicKey, digest, r, s)
}

func validFingerprint(fingerprint string) bool {
	if len(fingerprint) != sha256.Size*2 || strings.ToLower(fingerprint) != fingerprint {
		return false
	}
	decoded, err := hex.DecodeString(fingerprint)
	return err == nil && len(decoded) == sha256.Size
}

func decodeCanonicalBase64URL(value string, expectedBytes int) ([]byte, error) {
	decoded, err := base64.RawURLEncoding.DecodeString(value)
	if err != nil || len(decoded) != expectedBytes || base64.RawURLEncoding.EncodeToString(decoded) != value {
		return nil, errors.New("invalid canonical base64url")
	}
	return decoded, nil
}
