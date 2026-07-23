package crypto

import (
	"bytes"
	"testing"
)

func TestEncryptDecryptRoundTrip(t *testing.T) {
	key := make([]byte, 32)
	c, err := New(key)
	if err != nil {
		t.Fatal(err)
	}
	plain := []byte("supersecret root password")
	ct, err := c.Encrypt(plain)
	if err != nil {
		t.Fatal(err)
	}
	if ct == string(plain) {
		t.Fatal("ciphertext must not equal plaintext")
	}
	pt, err := c.Decrypt(ct)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(pt, plain) {
		t.Fatalf("round trip mismatch: %q != %q", pt, plain)
	}
}

func TestEncryptDifferentEachCall(t *testing.T) {
	c, _ := New(make([]byte, 32))
	a, _ := c.Encrypt([]byte("x"))
	b, _ := c.Encrypt([]byte("x"))
	if a == b {
		t.Fatal("random nonce should make ciphertexts differ")
	}
}

func TestDecryptGarbage(t *testing.T) {
	c, _ := New(make([]byte, 32))
	if _, err := c.Decrypt("not-base64!!!"); err == nil {
		t.Fatal("expected error on invalid base64")
	}
}

func TestNewBadKey(t *testing.T) {
	if _, err := New(make([]byte, 16)); err == nil {
		t.Fatal("expected error for non-32-byte key")
	}
}
