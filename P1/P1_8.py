#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def parse_1(string):

    pattern = re.compile("\w+ [A-Z]")
    return pattern.search(string)

def parse_2(string):

    pattern = re.compile("\w+@\w+\.\w+")
    return pattern.search(string)

def parse_3(string):

    pattern = re.compile("\d{4}([\s|\-])\d{4}\\1\d{4}\\1\d{4}")
    return pattern.search(string)
