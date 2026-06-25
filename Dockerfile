FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /geo-server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /geo-server /geo-server
EXPOSE 8080
ENTRYPOINT ["/geo-server"]
