package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type FpgaStatus struct {
    Temperature float64 `json:"temp_c"`
    DmaActive   bool    `json:"dma_active"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
    status := FpgaStatus{Temperature: 45.2, DmaActive: true}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(status)
}

func main() {
    http.HandleFunc("/fpga/status", statusHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
