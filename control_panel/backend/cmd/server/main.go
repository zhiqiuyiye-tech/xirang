package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/api"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/config"
	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/storage"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("config: %v", err)
	}
	store, err := db.Open(cfg.DBPath)
	if err != nil {
		log.Fatalf("db: %v", err)
	}
	defer store.Close()

	cipher, err := crypto.New(cfg.AESKey)
	if err != nil {
		log.Fatalf("crypto: %v", err)
	}

	// 启动恢复：中断的任务标记 failed
	if err := recoverInterrupted(context.Background(), store); err != nil {
		log.Printf("warn: recovery: %v", err)
	}

	// 首次启动种管理员
	if err := seedAdmin(context.Background(), store, cfg.AdminInitPassword); err != nil {
		log.Fatalf("seed admin: %v", err)
	}

	tk := auth.NewTokens(cfg.JWTSecret, cfg.JWTTTL,
		auth.WithIssuer(cfg.JWTIssuer),
		auth.WithAudience(cfg.JWTAudience),
	)
	limiter := auth.NewRateLimiter(cfg.RateLimitMaxFailures, cfg.RateLimitLockoutDuration, cfg.RateLimitWindow)
	defer limiter.Close()

	eng := tasks.NewEngine(store)
	eng.SetTaskTimeout(cfg.TaskTimeout)
	sshm := ssh.NewManager(cipher, cfg.SSHPoolSize, cfg.SSHIdleTimeout)
	defer sshm.Close() // stop idle-eviction goroutine + close pooled conns on exit
	ws := workers.NewService(store, cipher, sshm, eng)

	// K8s client: in-cluster only. Failure is fatal if REQUIRE_K8S is true.
	// Otherwise it is non-fatal for local development with k8s endpoints returning 503.
	k8sClient, err := k8s.NewClient()
	if err != nil {
		if cfg.RequireK8s {
			log.Fatalf("fatal: k8s client init failed (REQUIRE_K8S=true): %v", err)
		}
		log.Printf("warn: k8s client: %v (k8s endpoints disabled)", err)
		k8sClient = nil
	}
	k8s.RegisterK8sHandlers(eng, k8sClient)

	// Storage task handlers: sshm implements ssh.Runner. Registered after the
	// engine is created so the engine knows the type names before any storage
	// API endpoint submits a task.
	storage.RegisterStorageHandlers(eng, sshm, store)

	gin.SetMode(gin.ReleaseMode)
	r := api.NewRouter(tk, ws, store, eng, k8sClient, sshm,
		api.WithRateLimiter(limiter),
		api.WithCookieName(cfg.CookieName),
		api.WithCookieSecure(cfg.CookieSecure),
		api.WithCookieSameSite(cfg.CookieSameSite),
		api.WithCSRFCookieName(cfg.CSRFCookieName),
		api.WithCSRFHeaderName(cfg.CSRFHeaderName),
		api.WithRequireK8s(cfg.RequireK8s),
		api.WithTrustedProxies(cfg.TrustedProxies),
	)

	srv := &http.Server{Addr: cfg.ListenAddr, Handler: r}
	go func() {
		log.Printf("listening on %s", cfg.ListenAddr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}

func recoverInterrupted(ctx context.Context, store *db.Store) error {
	return tasks.NewEngine(store).Recover(ctx)
}

func seedAdmin(ctx context.Context, store *db.Store, initPw string) error {
	seeded, err := store.IsAdminSeeded(ctx)
	if err != nil {
		return err
	}
	if seeded {
		return nil
	}
	hash, err := auth.HashPassword(initPw)
	if err != nil {
		return err
	}
	return store.UpsertAdminPassword(ctx, "admin", hash)
}
