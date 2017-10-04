#!/usr/bin/env python
# -*- coding: utf-8 -*-

def n_fib(file_in, file_out):

    f = open(file_in)
    n = int(f.readline())
    f.close()

    if not n:

        f_o = open(file_out, "w")
        f_o.write(str(0))

    else:

        n -= 1 # No es f(0), por lo que hemos dado un paso
        n_0 = 1 # Actual
        n_1 = 1 # n-1 inicial
        n_2 = 0 # n-2 inicial

        while n > 0:

            n_0 = n_1 + n_2
            n_2 = n_1
            n_1 = n_0
            n -= 1

        f_o = open(file_out, "w")
        f_o.write(str(n_0))

if __name__ == "__main__":

    print("Introduce un archivo de entrada")
    input_file = input()
    print("Introduce un archivo de salida")
    output_file = input()

    n_fib(input_file, output_file)
