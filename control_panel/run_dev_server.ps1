$env:AES_KEY = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE="
$env:JWT_SECRET = "xirang-control-panel-dev-secret-key-2026"
$env:ADMIN_INIT_PASSWORD = "admin123456"
$env:DB_PATH = "control_panel_dev.db"
$env:LISTEN_ADDR = ":8090"
Set-Location control_panel/backend
go run ./cmd/server
