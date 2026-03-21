package main

import "fmt"

func main() {
	var sum uint64
	const n uint64 = 100000000

	for i := uint64(1); i <= n; i++ {
		sum += i
	}

	fmt.Println(sum)
}
