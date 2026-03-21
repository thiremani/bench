package main

import "fmt"

func main() {
	var sum uint64
	const n uint64 = 20000000

	for i := uint64(1); i <= n; i++ {
		sum += (i * 3) % 17
	}

	fmt.Println(sum)
}
