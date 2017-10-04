#!/usr/bin/env python
# -*- coding: utf-8 -*-

def bracket_parser(sequence):

    counter = 0

    for bracket in sequence:

        if bracket == '[':

            counter += 1

        else:

            counter -= 1

            if counter < 0:

                break

    if not counter:

        print("Secuencia balanceada")

    else:

        print("Secuencia no balanceada")

if __name__ == "__main__":

    seq = input()

    bracket_parser(seq)
