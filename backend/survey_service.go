package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, `{"service":"ENVR9 Go Survey Service","status":"active"}`)
	})

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"status":"healthy","timestamp":"%s"}`, time.Now().UTC())
	})

	fmt.Println("ENVR9 Go Survey Service starting on :8081")
	http.ListenAndServe(":8081", nil)
}
