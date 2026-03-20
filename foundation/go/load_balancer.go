package main

import "fmt"

func main() {
	loads := map[string]float64{"q-a": 0.31, "q-b": 0.75, "q-c": 0.44}
	best := ""
	bestLoad := 2.0
	for n, l := range loads {
		if l < bestLoad {
			best = n
			bestLoad = l
		}
	}
	fmt.Println("route to", best)
}
