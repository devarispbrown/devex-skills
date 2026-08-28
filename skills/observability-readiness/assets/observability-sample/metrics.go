// metrics.go — sample metrics instrumentation with Prometheus counters
// and a latency histogram.

package main

import "github.com/prometheus/client_golang/prometheus"

var (
	ordersTotal = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "orders_total",
		Help: "Total orders processed.",
	})
	orderLatency = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "order_latency_seconds",
		Help:    "Order processing latency.",
		Buckets: prometheus.DefBuckets,
	})
)
