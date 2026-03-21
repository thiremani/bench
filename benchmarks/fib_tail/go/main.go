package main

import "fmt"

func fibAux(n uint64, a uint64, b uint64) uint64 {
	if n == 0 {
		return a
	}
	return fibAux(n-1, b, a+b)
}

func fib(n uint64) uint64 {
	return fibAux(n, 0, 1)
}

func main() {
	var sum uint64
	const repeats uint64 = 1000000

	for i := uint64(0); i < repeats; i++ {
		sum += fib(32 + (i % 2))
	}

	fmt.Println(sum)
}
