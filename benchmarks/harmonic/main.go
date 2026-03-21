package main

import "fmt"

func main() {
	var sum float64
	const n uint64 = 10000001

	for i := uint64(1); i < n; i++ {
		sum += 1.0 / float64(i)
	}

	fmt.Printf("%.6f\n", sum)
}
