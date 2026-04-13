package main

import (
    "fmt"
    "log"
    "net/http"
)

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"status":"healthy","service":"ptof-1.6"}`)
}

func main() {
    http.HandleFunc("/health", healthHandler)
    log.Println("Go health service listening on :8081")
    log.Fatal(http.ListenAndServe(":8081", nil))
}
