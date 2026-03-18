package main

import (
	"fmt"
	"os"
	"runtime"
)

func main() {
	fmt.Printf("ENVR Go %s %s/%s\n", runtime.Version(), runtime.GOOS, runtime.GOARCH)
	fmt.Println("cwd:", mustWd())
}

func mustWd() string {
	wd, err := os.Getwd()
	if err != nil {
		return "error"
	}
	return wd
}
