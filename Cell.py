#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2025 Michael S. Kenniston

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# Define the cells of the playing area for the "Queens" game


WHITE = 'W'
YELLOW = 'Y'
ORANGE = 'O'
RED = 'R'
PINK = 'P'
VIOLET = 'V'
BLUE = 'B'
SKY_BLUE = 'S'
LIME = 'L'
GRAY = 'G'
ALL_COLORS = [WHITE, YELLOW, ORANGE, RED, PINK,
              VIOLET, BLUE, SKY_BLUE, LIME, GRAY]


class Cell():
    def __init__(self, row, col, color):
        if color not in ALL_COLORS:
            raise BaseException("illegal color %s" % color)
        self._row = row
        self._col = col
        self._color = color

    def row(self):
        return self._row

    def col(self):
        return self._col

    def color(self):
        return self._color
