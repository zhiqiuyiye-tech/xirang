package auth

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"os"
	"strings"
	"testing"
)

func TestCanonicalizeP256PublicKeyPEM(t *testing.T) {
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	der, err := x509.MarshalPKIXPublicKey(&privateKey.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	input := string(pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: der}))

	parsed, canonicalPEM, fingerprint, err := CanonicalizeP256PublicKeyPEM(input)
	if err != nil {
		t.Fatalf("CanonicalizeP256PublicKeyPEM() error = %v", err)
	}
	if parsed.Curve != elliptic.P256() || parsed.X.Cmp(privateKey.X) != 0 || parsed.Y.Cmp(privateKey.Y) != 0 {
		t.Fatal("parsed key does not match the generated P-256 public key")
	}
	canonicalBlock, _ := pem.Decode([]byte(canonicalPEM))
	if canonicalBlock == nil || canonicalBlock.Type != "PUBLIC KEY" {
		t.Fatalf("canonical PEM has invalid block: %q", canonicalPEM)
	}
	canonicalDER, err := x509.MarshalPKIXPublicKey(parsed)
	if err != nil {
		t.Fatal(err)
	}
	if string(canonicalBlock.Bytes) != string(canonicalDER) {
		t.Fatal("canonical PEM does not contain canonical SPKI DER")
	}
	digest := sha256.Sum256(canonicalDER)
	if fingerprint != hex.EncodeToString(digest[:]) {
		t.Fatalf("fingerprint = %q, want %q", fingerprint, hex.EncodeToString(digest[:]))
	}
}

func TestCanonicalizeP256PublicKeyPEMRejectsInvalidKeys(t *testing.T) {
	p384, err := ecdsa.GenerateKey(elliptic.P384(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	der, err := x509.MarshalPKIXPublicKey(&p384.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	p384PEM := string(pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: der}))

	for name, input := range map[string]string{
		"empty":         "",
		"malformed PEM": "-----BEGIN PUBLIC KEY-----\nnot-der\n-----END PUBLIC KEY-----",
		"wrong curve":   p384PEM,
		"private block": string(pem.EncodeToMemory(&pem.Block{Type: "PRIVATE KEY", Bytes: []byte("not a public key")})),
	} {
		t.Run(name, func(t *testing.T) {
			if _, _, _, err := CanonicalizeP256PublicKeyPEM(input); err == nil {
				t.Fatal("expected invalid public key to be rejected")
			}
		})
	}
}

func TestBuildChallengeMessageUsesPurposeSpecificDomain(t *testing.T) {
	fingerprint := strings.Repeat("a", 64)
	newFingerprint := strings.Repeat("b", 64)
	nonce := strings.Repeat("A", 43) // canonical base64url for 32 zero bytes
	version := int64(7)
	cases := []struct {
		name    string
		context ChallengeContext
		kind    ProofKind
		want    string
	}{
		{
			name:    "login",
			context: ChallengeContext{ID: "AQIDBAUGBwgJCgsMDQ4PEA", Nonce: nonce, Purpose: PurposeLogin, AuthVersion: version, KeyFingerprint: fingerprint},
			kind:    ProofLogin,
			want:    "xirang-control-panel-login-v1\nAQIDBAUGBwgJCgsMDQ4PEA\n" + nonce + "\n7\n" + fingerprint,
		},
		{
			name:    "bootstrap",
			context: ChallengeContext{ID: "AQIDBAUGBwgJCgsMDQ4PEA", Nonce: nonce, Purpose: PurposeBootstrap, AuthVersion: version, NewKeyFingerprint: newFingerprint},
			kind:    ProofBootstrap,
			want:    "xirang-control-panel-bootstrap-v1\nAQIDBAUGBwgJCgsMDQ4PEA\n" + nonce + "\n7\n" + newFingerprint,
		},
		{
			name:    "current key rotation authorization",
			context: ChallengeContext{ID: "AQIDBAUGBwgJCgsMDQ4PEA", Nonce: nonce, Purpose: PurposeKeyRotate, AuthVersion: version, KeyFingerprint: fingerprint, NewKeyFingerprint: newFingerprint},
			kind:    ProofKeyRotate,
			want:    "xirang-control-panel-key-rotate-v1\nAQIDBAUGBwgJCgsMDQ4PEA\n" + nonce + "\n7\n" + fingerprint + "\n" + newFingerprint,
		},
		{
			name:    "new key proof",
			context: ChallengeContext{ID: "AQIDBAUGBwgJCgsMDQ4PEA", Nonce: nonce, Purpose: PurposeKeyRotate, AuthVersion: version, KeyFingerprint: fingerprint, NewKeyFingerprint: newFingerprint},
			kind:    ProofNewKey,
			want:    "xirang-control-panel-new-key-proof-v1\nAQIDBAUGBwgJCgsMDQ4PEA\n" + nonce + "\n7\n" + newFingerprint,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := BuildChallengeMessage(tc.context, tc.kind)
			if err != nil {
				t.Fatalf("BuildChallengeMessage() error = %v", err)
			}
			if string(got) != tc.want {
				t.Fatalf("message mismatch\n got: %q\nwant: %q", got, tc.want)
			}
		})
	}
}

func TestBuildChallengeMessageRejectsPurposeMismatch(t *testing.T) {
	ctx := ChallengeContext{
		ID: "AQIDBAUGBwgJCgsMDQ4PEA", Nonce: strings.Repeat("A", 43),
		Purpose: PurposeLogin, AuthVersion: 1, KeyFingerprint: strings.Repeat("a", 64),
	}
	if _, err := BuildChallengeMessage(ctx, ProofKeyRotate); err == nil {
		t.Fatal("expected purpose mismatch to be rejected")
	}
}

func TestDecodeCanonicalRawSignature(t *testing.T) {
	raw := make([]byte, 64)
	for i := range raw {
		raw[i] = byte(i + 1)
	}
	encoded := base64.RawURLEncoding.EncodeToString(raw)
	decoded, err := DecodeCanonicalRawSignature(encoded)
	if err != nil {
		t.Fatalf("DecodeCanonicalRawSignature() error = %v", err)
	}
	if string(decoded[:]) != string(raw) {
		t.Fatal("decoded signature differs from original r||s bytes")
	}

	for name, invalid := range map[string]string{
		"padded":     base64.URLEncoding.EncodeToString(raw),
		"short":      base64.RawURLEncoding.EncodeToString(raw[:63]),
		"long":       base64.RawURLEncoding.EncodeToString(append(raw, 0)),
		"standard64": "+" + base64.RawURLEncoding.EncodeToString(raw)[1:],
	} {
		t.Run(name, func(t *testing.T) {
			if _, err := DecodeCanonicalRawSignature(invalid); err == nil {
				t.Fatal("expected non-canonical signature to be rejected")
			}
		})
	}
}

func TestVerifyP256DigestSignature(t *testing.T) {
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	digest := sha256.Sum256([]byte("xirang test message"))
	r, s, err := ecdsa.Sign(rand.Reader, privateKey, digest[:])
	if err != nil {
		t.Fatal(err)
	}
	var raw [64]byte
	r.FillBytes(raw[:32])
	s.FillBytes(raw[32:])
	if !VerifyP256DigestSignature(&privateKey.PublicKey, digest[:], raw) {
		t.Fatal("valid P-256 signature was rejected")
	}
	otherDigest := sha256.Sum256([]byte("different message"))
	if VerifyP256DigestSignature(&privateKey.PublicKey, otherDigest[:], raw) {
		t.Fatal("signature for another digest was accepted")
	}

	invalidR := [64]byte{}
	elliptic.P256().Params().N.FillBytes(invalidR[:32])
	invalidR[63] = 1
	if VerifyP256DigestSignature(&privateKey.PublicKey, digest[:], invalidR) {
		t.Fatal("r equal to curve order was accepted")
	}
	invalidS := [64]byte{}
	invalidS[31] = 1
	elliptic.P256().Params().N.FillBytes(invalidS[32:])
	if VerifyP256DigestSignature(&privateKey.PublicKey, digest[:], invalidS) {
		t.Fatal("s equal to curve order was accepted")
	}
	zeroRS := [64]byte{}
	if VerifyP256DigestSignature(&privateKey.PublicKey, digest[:], zeroRS) {
		t.Fatal("zero r and s were accepted")
	}
}

func TestP256GoSignatureInteropFixture(t *testing.T) {
	data, err := os.ReadFile("testdata/p256-login-vector.json")
	if err != nil {
		t.Fatalf("read fixed P-256 vector: %v", err)
	}
	var vector struct {
		PrivateKeyPEM        string `json:"private_key_pem"`
		PublicKeyPEM         string `json:"public_key_pem"`
		Message              string `json:"message"`
		DigestHex            string `json:"digest_hex"`
		Signature            string `json:"signature"`
		JSSignature          string `json:"js_signature"`
		BrowserPrivateKeyPEM string `json:"browser_generated_private_key_pem"`
		BrowserPublicKeyPEM  string `json:"browser_generated_public_key_pem"`
		BrowserFingerprint   string `json:"browser_generated_fingerprint"`
	}
	if err := json.Unmarshal(data, &vector); err != nil {
		t.Fatalf("decode fixed P-256 vector: %v", err)
	}
	publicKey, _, fingerprint, err := CanonicalizeP256PublicKeyPEM(vector.PublicKeyPEM)
	if err != nil {
		t.Fatalf("parse fixed public key: %v", err)
	}
	privateBlock, _ := pem.Decode([]byte(vector.PrivateKeyPEM))
	if privateBlock == nil || privateBlock.Type != "PRIVATE KEY" {
		t.Fatal("fixed private key is not PKCS#8 PEM")
	}
	parsedPrivate, err := x509.ParsePKCS8PrivateKey(privateBlock.Bytes)
	if err != nil {
		t.Fatalf("parse fixed private key: %v", err)
	}
	privateKey, ok := parsedPrivate.(*ecdsa.PrivateKey)
	if !ok || privateKey.Curve != elliptic.P256() {
		t.Fatal("fixed private key is not ECDSA P-256")
	}
	if privateKey.X.Cmp(publicKey.X) != 0 || privateKey.Y.Cmp(publicKey.Y) != 0 {
		t.Fatal("fixed private and public key do not match")
	}
	if vector.Message != "xirang-control-panel-login-v1\nAQIDBAUGBwgJCgsMDQ4PEA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n1\n"+fingerprint {
		t.Fatalf("unexpected fixed signed message: %q", vector.Message)
	}
	digest := sha256.Sum256([]byte(vector.Message))
	if hex.EncodeToString(digest[:]) != vector.DigestHex {
		t.Fatalf("digest = %x, want %s", digest, vector.DigestHex)
	}
	signature, err := DecodeCanonicalRawSignature(vector.Signature)
	if err != nil {
		t.Fatalf("decode fixed signature: %v", err)
	}
	if !VerifyP256DigestSignature(publicKey, digest[:], signature) {
		t.Fatal("Go rejected the fixed Go interoperability signature")
	}
	jsSignature, err := DecodeCanonicalRawSignature(vector.JSSignature)
	if err != nil {
		t.Fatalf("decode fixed JavaScript signature: %v", err)
	}
	if !VerifyP256DigestSignature(publicKey, digest[:], jsSignature) {
		t.Fatal("Go rejected the fixed JavaScript interoperability signature")
	}
	browserPublicKey, _, browserFingerprint, err := CanonicalizeP256PublicKeyPEM(vector.BrowserPublicKeyPEM)
	if err != nil {
		t.Fatalf("parse browser-generated public key: %v", err)
	}
	browserPrivateBlock, _ := pem.Decode([]byte(vector.BrowserPrivateKeyPEM))
	if browserPrivateBlock == nil || browserPrivateBlock.Type != "PRIVATE KEY" {
		t.Fatal("browser-generated private key is not PKCS#8 PEM")
	}
	browserParsed, err := x509.ParsePKCS8PrivateKey(browserPrivateBlock.Bytes)
	if err != nil {
		t.Fatalf("Go cannot parse browser-generated PKCS#8: %v", err)
	}
	browserPrivateKey, ok := browserParsed.(*ecdsa.PrivateKey)
	if !ok || browserPrivateKey.Curve != elliptic.P256() || browserPrivateKey.X.Cmp(browserPublicKey.X) != 0 || browserPrivateKey.Y.Cmp(browserPublicKey.Y) != 0 {
		t.Fatal("browser-generated PKCS#8 does not match its P-256 public key")
	}
	if browserFingerprint != vector.BrowserFingerprint {
		t.Fatalf("browser fingerprint = %s, want %s", browserFingerprint, vector.BrowserFingerprint)
	}
}
