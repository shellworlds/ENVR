// SN-112BA Post-quantum handshake (Go). Main developer: shellworlds.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/rand"
)

func kyberSimKeygen() ([]byte, []byte) {
	pk := make([]byte, 32)
	sk := make([]byte, 32)
	rand.Read(pk)
	rand.Read(sk)
	return pk, sk
}

func kyberSimEncaps(pk []byte) ([]byte, []byte) {
	r := make([]byte, 32)
	rand.Read(r)
	h := sha256.New()
	h.Write(append(pk, r...))
	shared := h.Sum(nil)
	h.Reset()
	h.Write(append(r, pk...))
	ct := h.Sum(nil)
	return ct, shared
}

func kyberSimDecaps(sk, ct []byte) []byte {
	h := sha256.New()
	h.Write(append(sk, ct...))
	return h.Sum(nil)
}

func main() {
	pk, sk := kyberSimKeygen()
	ct, sharedA := kyberSimEncaps(pk)
	sharedB := kyberSimDecaps(sk, ct)
	fmt.Println("SN-112BA Go handshake OK:", hex.EncodeToString(sharedA)[:16] == hex.EncodeToString(sharedB)[:16])
}
