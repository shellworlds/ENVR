package main

import "fmt"

func main() {
	nodes := []string{"q-a", "q-b", "q-c"}
	for _, n := range nodes {
		fmt.Println("discovered", n)
	}
}
