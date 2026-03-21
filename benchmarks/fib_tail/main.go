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
	fmt.Println(fib(32))
}
