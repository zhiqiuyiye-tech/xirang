FROM --platform=$BUILDPLATFORM golang:alpine AS build
WORKDIR /src
# golang:alpine tracks the latest stable Go. GOTOOLCHAIN=auto lets the build
# fetch the exact version go.mod requires if the image's Go is older.
ENV GOTOOLCHAIN=auto
ENV GOPROXY=https://goproxy.cn,direct
ARG TARGETOS=linux
ARG TARGETARCH=arm64
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -ldflags="-s -w" -o /out/server ./cmd/server

FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata && \
    addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /sbin/nologin -D appuser && \
    mkdir -p /data /tmp && \
    chown -R appuser:appgroup /data /tmp

WORKDIR /app
COPY --from=build --chown=appuser:appgroup /out/server /app/server
USER 10001:10001
ENV DB_PATH=/data/control_panel.db
ENV LISTEN_ADDR=:8080
EXPOSE 8080
ENTRYPOINT ["/app/server"]
