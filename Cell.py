#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2025 Michael S. Kenniston.  All rights reserved.

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
