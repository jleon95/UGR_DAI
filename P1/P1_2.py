#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

def mergesort(unordered):

    elements = list(unordered)

    if len(elements) < 2:

        return elements

    else:

        middle = len(elements)//2

        left_half = mergesort(elements[:middle])
        right_half = mergesort(elements[middle:])

        if(left_half[-1] <= right_half[0]):

            left_half.extend(right_half)
            return left_half

        elements = merge(left_half, right_half)

        return elements

def merge(left_half, right_half):

    result = []

    while left_half and right_half:

        if(left_half[0] <= right_half[0]):

            result.append(left_half[0])
            left_half.pop(0)

        else:

            result.append(right_half[0])
            right_half.pop(0)


    if left_half:

        result.extend(left_half)

    else:

        result.extend(right_half)

    return result

def insertion_sort(unordered):

    elements = list(unordered)

    if elements:

        for i in range(1, len(elements)):

            current = i

            j = i - 1

            while j >= 0 and elements[j] > elements[current]:

                j -= 1

            value = elements[current]
            elements.remove(value)
            elements.insert(j+1,value)

if __name__ == "__main__":

    random_list = random.sample(range(0, 1000), 1000)

    mergesort_before = time.clock()
    mergesort(random_list)
    mergesort_after = time.clock()

    insertion_before = time.clock()
    insertion_sort(random_list)
    insertion_after = time.clock()

    print("Tiempo Mergesort " + str(mergesort_after-mergesort_before))
    print("Tiempo Inserción " + str(insertion_after-insertion_before))
