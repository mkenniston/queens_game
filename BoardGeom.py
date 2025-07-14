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

# Define the playing area for the "Queens" game
# The "BoardGeom" object contains all the immutable information.


from Cell import Cell, ALL_COLORS
from Group import RowGroup, ColGroup, ColorGroup


class BoardGeom():
    def __init__(self, description):
        desc_lines = self._parse(description)
        self._size = len(desc_lines)
        self._cells = []

        # Create all the groups.
        self._row_groups = []
        group_number = 0
        for row in range(self._size):
            self._row_groups.append(
                RowGroup(self, group_number, "row-%d" % row))
            group_number += 1
        self._col_groups = []
        for col in range(self._size):
            self._col_groups.append(
                ColGroup(self, group_number, "col-%d" % col))
            group_number += 1
        self._groups = self._row_groups + self._col_groups
        self._color_groups = {}
        for color in ALL_COLORS:
            g = ColorGroup(self, group_number, "color-%s" % color)
            self._color_groups[color] = g
            self._groups.append(g)
            group_number += 1

        # Fill in the colors from the input file.
        for row in range(self._size):
            this_row = []
            for col in range(self._size):
                color = desc_lines[row][col]
                cell = Cell(row, col, color)
                self._row_groups[row].add(cell)
                self._col_groups[col].add(cell)
                self._color_groups[color].add(cell)
                this_row.append(cell)
            self._cells.append(this_row)

    def size(self):
        return self._size

    def groups(self):
        return self._groups

    def row_group(self, row):
        return self._row_groups[row]

    def col_group(self, col):
        return self._col_groups[col]

    def color_group(self, color):
        return self._color_groups[color]

    def color_groups(self):
        return self._color_groups.values()

    def get_cell_color(self, row, col):
        # print("DEBUG: getting color for (%d, %d)" % (row, col))
        cell = self._cells[row][col]
        # print("       found color %s" % cell.color())
        return cell.color()

    def _parse(self, description):
        # do the initial parsing
        lines = []
        for line in description.upper().split('\n'):
            line = line.strip()
            if len(line) < 1 or line[0] == '#':
                continue
            # print('->> "%s" len %d' % (line, len(line)))
            lines.append(line)
        # print("input read is:")
        # print(lines)

        # validate the geometry
        size = len(lines)
        for line in lines:
            if len(line) != size:
                raise BaseException(
                    'line "%s" has incorrect length %d; it should be %d' %
                    (line, len(line), size))

        # validate the coding
        for line in lines:
            for char in line:
                if char not in ALL_COLORS:
                    raise BaseException(
                       'line "%s" has invalid color "%s"' % (line, char))
        return lines
