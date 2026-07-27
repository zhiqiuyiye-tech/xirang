FROM golang:alpine AS build
WORKDIR /src
# golang:alpine tracks the latest stable Go. GOTOOLCHAIN=auto lets the build
# fetch the exact version go.mod requires if the image's Go is older.
ENV GOTOOLCHAIN=auto
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/server ./cmd/server

FROM alpine:3.20
RUN apk add --no-cache ca-certificates
WORKDIR /app
COPY --from=build /out/server /app/server
RUN mkdir -p /data
ENV DB_PATH=/data/control_panel.db
ENV LISTEN_ADDR=:8080
EXPOSE 8080
ENTRYPOINT ["/app/server"]
