package auth

import (
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

func HashPassword(plain string) (string, error) {
	b, err := bcrypt.GenerateFromPassword([]byte(plain), bcrypt.DefaultCost)
	return string(b), err
}

func CheckPassword(hash, plain string) bool {
	return bcrypt.CompareHashAndPassword([]byte(hash), []byte(plain)) == nil
}

type Claims struct {
	AdminID     int64  `json:"admin_id"`
	Username    string `json:"username"`
	AuthVersion int64  `json:"auth_version"`
	jwt.RegisteredClaims
}

type Tokens struct {
	secret   []byte
	ttl      time.Duration
	issuer   string
	audience string
}

type TokenOption func(*Tokens)

func WithIssuer(issuer string) TokenOption {
	return func(t *Tokens) {
		t.issuer = issuer
	}
}

func WithAudience(audience string) TokenOption {
	return func(t *Tokens) {
		t.audience = audience
	}
}

func NewTokens(jwtSecret string, ttl time.Duration, opts ...TokenOption) *Tokens {
	t := &Tokens{
		secret:   []byte(jwtSecret),
		ttl:      ttl,
		issuer:   "xirang-control-panel",
		audience: "xirang-control-panel-api",
	}
	for _, opt := range opts {
		opt(t)
	}
	return t
}

func (t *Tokens) TTL() time.Duration {
	return t.ttl
}

func (t *Tokens) Issue(adminID int64, username string, authVersion ...int64) (string, error) {
	var ver int64 = 1
	if len(authVersion) > 0 && authVersion[0] > 0 {
		ver = authVersion[0]
	}
	now := time.Now().UTC()
	c := Claims{
		AdminID:     adminID,
		Username:    username,
		AuthVersion: ver,
		RegisteredClaims: jwt.RegisteredClaims{
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(t.ttl)),
			Issuer:    t.issuer,
			Audience:  jwt.ClaimStrings{t.audience},
		},
	}
	tok := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	return tok.SignedString(t.secret)
}

func (t *Tokens) Parse(tokenStr string) (Claims, error) {
	var c Claims
	parserOpts := []jwt.ParserOption{
		jwt.WithValidMethods([]string{jwt.SigningMethodHS256.Alg()}),
	}
	if t.issuer != "" {
		parserOpts = append(parserOpts, jwt.WithIssuer(t.issuer))
	}
	if t.audience != "" {
		parserOpts = append(parserOpts, jwt.WithAudience(t.audience))
	}

	parsedToken, err := jwt.ParseWithClaims(tokenStr, &c, func(tok *jwt.Token) (interface{}, error) {
		if tok.Method.Alg() != jwt.SigningMethodHS256.Alg() {
			return nil, fmt.Errorf("unexpected signing method %q, only HS256 allowed", tok.Method.Alg())
		}
		return t.secret, nil
	}, parserOpts...)

	if err != nil {
		return Claims{}, err
	}
	if !parsedToken.Valid {
		return Claims{}, errors.New("invalid token")
	}
	return c, nil
}
