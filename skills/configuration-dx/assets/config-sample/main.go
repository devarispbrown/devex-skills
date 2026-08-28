// Sample CLI: flags duplicate env vars for the same settings.
package main

import (
	"flag"
	"os"
)

func main() {
	apiKey := flag.String("api-key", "changeme", "API key (or set API_KEY)")
	timeout := flag.Int("timeout", 60, "request timeout in seconds (or set TIMEOUT)")
	flag.Parse()
	_ = os.Getenv("API_KEY")
	_ = os.Getenv("TIMEOUT")
	_ = apiKey
	_ = timeout
}
