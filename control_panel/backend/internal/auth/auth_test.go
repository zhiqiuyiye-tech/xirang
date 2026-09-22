package auth

import (
	"testing"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

func TestHashAndCheckPassword(t *testing.T) {
	h, err := HashPassword("hunter2")
	if err != nil {
		t.Fatal(err)
	}
	if !CheckPassword(h, "hunter2") {
		t.Fatal("check should pass for correct password")
	}
	if CheckPassword(h, "wrong") {
		t.Fatal("check should fail for wrong password")
	}
}

func TestTokenIssueAndParse(t *testing.T) {
	tk := NewTokens("secret", time.Hour)
	tok, err := tk.Issue(7, "admin", 2)
	if err != nil {
		t.Fatal(err)
	}
	c, err := tk.Parse(tok)
	if err != nil {
		t.Fatal(err)
	}
	if c.AdminID != 7 || c.Username != "admin" || c.AuthVersion != 2 {
		t.Fatalf("claims=%+v", c)
	}
}

func TestTokenParseBadSignature(t *testing.T) {
	tk := NewTokens("secret", time.Hour)
	if _, err := tk.Parse("garbage.token.here"); err == nil {
		t.Fatal("expected parse error")
	}
}

func TestTokenParseExpired(t *testing.T) {
	tk := NewTokens("secret", -time.Hour) // 已过期
	tok, _ := tk.Issue(1, "admin")
	if _, err := tk.Parse(tok); err == nil {
		t.Fatal("expected expiry error")
	}
}

func TestTokenParseWrongIssuerOrAudience(t *testing.T) {
	tk := NewTokens("secret", time.Hour, WithIssuer("good-issuer"), WithAudience("good-audience"))
	tok, err := tk.Issue(1, "admin")
	if err != nil {
		t.Fatal(err)
	}

	// Parser with mismatched issuer
	badIssuerTk := NewTokens("secret", time.Hour, WithIssuer("wrong-issuer"), WithAudience("good-audience"))
	if _, err := badIssuerTk.Parse(tok); err == nil {
		t.Fatal("expected error with mismatched issuer")
	}

	// Parser with mismatched audience
	badAudTk := NewTokens("secret", time.Hour, WithIssuer("good-issuer"), WithAudience("wrong-audience"))
	if _, err := badAudTk.Parse(tok); err == nil {
		t.Fatal("expected error with mismatched audience")
	}
}

func TestTokenParseRejectWrongAlgorithm(t *testing.T) {
	// Sign with "none" or HS384/HS512 instead of HS256
	c := Claims{
		AdminID:     1,
		Username:    "admin",
		AuthVersion: 1,
		RegisteredClaims: jwt.RegisteredClaims{
			IssuedAt:  jwt.NewNumericDate(time.Now().UTC()),
			ExpiresAt: jwt.NewNumericDate(time.Now().UTC().Add(time.Hour)),
			Issuer:    "xirang-control-panel",
			Audience:  jwt.ClaimStrings{"xirang-control-panel-api"},
		},
	}
	tok := jwt.NewWithClaims(jwt.SigningMethodHS384, c)
	signed, err := tok.SignedString([]byte("secret"))
	if err != nil {
		t.Fatal(err)
	}

	tk := NewTokens("secret", time.Hour)
	if _, err := tk.Parse(signed); err == nil {
		t.Fatal("expected error when token algorithm is HS384 instead of HS256")
	}
}
