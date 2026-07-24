package auth

import (
	"errors"
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
	AdminID  int64  `json:"admin_id"`
	Username string `json:"username"`
	jwt.RegisteredClaims
}

type Tokens struct {
	secret []byte
	ttl    time.Duration
}

func NewTokens(jwtSecret string, ttl time.Duration) *Tokens {
	return &Tokens{secret: []byte(jwtSecret), ttl: ttl}
}

func (t *Tokens) Issue(adminID int64, username string) (string, error) {
	now := time.Now().UTC()
	c := Claims{
		AdminID:  adminID,
		Username: username,
		RegisteredClaims: jwt.RegisteredClaims{
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(t.ttl)),
		},
	}
	tok := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	return tok.SignedString(t.secret)
}

func (t *Tokens) Parse(tokenStr string) (Claims, error) {
	var c Claims
	_, err := jwt.ParseWithClaims(tokenStr, &c, func(tok *jwt.Token) (interface{}, error) {
		if _, ok := tok.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errors.New("unexpected signing method")
		}
		return t.secret, nil
	})
	if err != nil {
		return Claims{}, err
	}
	return c, nil
}
