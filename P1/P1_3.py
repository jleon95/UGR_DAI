#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def eratosthenes(n):

    numbers = [x for x in range(2,n)]
    primes = []

    while numbers:

        primes.append(numbers[0])

        for n in numbers:

            if n % primes[-1] == 0:

                numbers.remove(n)

    return primes

if __name__ == "__main__":

    print("Introduce un número")
    number = int(input())

    print(eratosthenes(number))
