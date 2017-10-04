#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def guess():
    chosen = random.randint(1,100)
    for n in range(10):
        print("Introduce un número:")
        number = int(input())
        if(number > chosen):
            print("El número buscado es menor")
        elif(number < chosen):
            print("El número buscado es mayor")
        else:
            print("Correcto")
            break

if __name__ == "__main__":

    guess()
