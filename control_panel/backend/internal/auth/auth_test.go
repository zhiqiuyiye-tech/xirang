package auth

import (
	"testing"
	"time"
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
	tok, err := tk.Issue(7, "admin")
	if err != nil {
		t.Fatal(err)
	}
	c, err := tk.Parse(tok)
	if err != nil {
		t.Fatal(err)
	}
	if c.AdminID != 7 || c.Username != "admin" {
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
