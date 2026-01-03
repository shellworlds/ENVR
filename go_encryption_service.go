// Go: Client Encryption Microservice
// High-performance encryption service
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type Client struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Algorithm string    `json:"algorithm"`
	CreatedAt time.Time `json:"created_at"`
}

type EncryptionRequest struct {
	ClientID  string `json:"client_id"`
	Plaintext string `json:"plaintext"`
}

type EncryptionResponse struct {
	Ciphertext string    `json:"ciphertext"`
	KeyID      string    `json:"key_id"`
	Algorithm  string    `json:"algorithm"`
	Timestamp  time.Time `json:"timestamp"`
}

func encryptAES256GCM(plaintext []byte) (string, error) {
	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		return "", err
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return "", err
	}

	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func main() {
	http.HandleFunc("/encrypt", func(w http.ResponseWriter, r *http.Request) {
		var req EncryptionRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		ciphertext, err := encryptAES256GCM([]byte(req.Plaintext))
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		response := EncryptionResponse{
			Ciphertext: ciphertext,
			Algorithm:  "AES-256-GCM",
			Timestamp:  time.Now(),
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	log.Println("🚀 Encryption service running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
