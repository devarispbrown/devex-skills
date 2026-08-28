// service.go — sample HTTP service with structured logging, request IDs,
// health endpoints, and trace spans. Slog + OpenTelemetry + Prometheus.

package main

import (
	"context"
	"log/slog"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/trace"
)

var requestCounter = prometheus.NewCounter(prometheus.CounterOpts{
	Name: "http_requests_total",
	Help: "Total HTTP requests handled.",
})

func handleOrder(w http.ResponseWriter, r *http.Request) {
	requestID := r.Header.Get("X-Request-ID")
	tracer := otel.Tracer("orders")
	ctx, span := tracer.Start(context.Background(), "handle_order")
	defer span.End()

	slog.Info("handling order",
		"request_id", requestID,
		"method", r.Method,
		"path", r.URL.Path,
	)
	requestCounter.Inc()
	w.WriteHeader(http.StatusOK)
	_ = ctx
}

func healthz(w http.ResponseWriter, _ *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func readyz(w http.ResponseWriter, _ *http.Request) {
	if databaseReachable() {
		w.WriteHeader(http.StatusOK)
		return
	}
	w.WriteHeader(http.StatusServiceUnavailable)
}

func databaseReachable() bool { return true }
