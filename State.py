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

# Define the current state of a "Queens" game
# The "State" object contains all the mutable information.


from Util import FatalException
from Geometry import Geometry

FREE = ' '
BLOCKED = 'x'
QUEEN = 'Q'
ALL_STATES = [FREE, BLOCKED, QUEEN]


class State():
    def __init__(self, arg):
        if isinstance(arg, Geometry):
            self._init_new(arg)
        elif isinstance(arg, State):
            self._init_copy(arg)
        else:
            raise FatalException("illegal arg type %s" % type(arg))
        return

    def _init_new(self, geom):
        self._geom = geom
        self._groups = self._geom.groups()
        size = self._geom.size()
        self._cell_states = [[FREE] * size for i in range(size)]
        self.recalc_free_cells()
        self._num_queens = 0

    def _init_copy(self, orig):
        # "self" is the new copy
        self._geom = orig._geom
        self._groups = orig._groups
        size = self._geom.size()
        self._cell_states = [[orig._cell_states[row][col]
                              for col in range(size)]
                             for row in range(size)]
        self.recalc_free_cells()
        self._num_queens = orig._num_queens

    def geom(self):
        return self._geom

    def num_queens(self):
        return self._num_queens

    def num_total_free_cells(self):
        return self._num_total_free_cells

    def recalc_free_cells(self):
        self._free_cells = []
        self._num_total_free_cells = 0
        for g in self._groups:
            free_in_this_group = self.get_cells_in_group(g, state=FREE)
            self._free_cells.append(free_in_this_group)
            self._num_total_free_cells += len(free_in_this_group)

    def get_cells_in_group(self, group, row=None, col=None, state=None):
        result = []
        for cell in group.cells():
            if row is not None and cell.row() != row:
                continue
            if col is not None and cell.col() != col:
                continue
            if (state is not None and
                    self._cell_states[cell.row()][cell.col()] != state):
                continue
            result.append(cell)
        return result

    def num_free_cells_in_group(self, group_number):
        return len(self._free_cells[group_number])

    def free_cells_in_group(self, group_number):
        return self._free_cells[group_number]

    def cell_state(self, row, col):
        return self._cell_states[row][col]

    def _set_blocked_by_queen(self, row, col):
        size = self._geom.size()

        # Block all immediate neighbors of the new queen.
        for row_inc in [-1, 0, +1]:
            for col_inc in [-1, 0, +1]:
                if row_inc == 0 and col_inc == 0:
                    continue  # don't block queen's own cell
                self.set_cell_state(row + row_inc, col + col_inc, BLOCKED)
                # print("TRACE nbr %d, %d" % (row + row_inc, col + col_inc))

        # Block all other cells in the same col as the new queen.
        for r in range(size):
            if r == row:
                continue
            self.set_cell_state(r, col, BLOCKED)
            # print("TRACE col %d, %d" % (r, col))

        # Block all other cells in the same row as the new queen.
        for c in range(size):
            if c == col:
                continue
            self.set_cell_state(row, c, BLOCKED)
            # print("TRACE row %d, %d" % (row, c))

        # Block all other cells the same color as the new queen's cell.
        geom = self._geom
        color = geom.cell_color(row, col)
        group = geom.color_group(color)
        for cell in group.cells():
            if cell.row() == row and cell.col() == col:
                continue  # don't block queen's own cell
            self.set_cell_state(cell.row(), cell.col(), BLOCKED)
            # print("TRACE %s, %d, %d" % (color, cell.row(), cell.col()))

    def set_cell_state(self, row, col, new_state):
        size = self._geom.size()
        if row < 0 or row >= size or col < 0 or col >= size:
            return  # make it easier to block cells adjacent to new queen
        if new_state not in ALL_STATES:
            raise FatalException("illegal state %s" % new_state)
        old_state = self._cell_states[row][col]
        if new_state == old_state:
            return  # harmless no-op
        if row == 0 and col == 1:
            print("CHANGING %d, %d to %s" % (row, col, new_state))
        if old_state == BLOCKED:
            raise FatalException("attempt to unblock (%d, %d)" % (row, col))
        if old_state == QUEEN:
            raise FatalException("attempt to unqueen (%d, %d)" % (row, col))

        self._cell_states[row][col] = new_state
        if new_state == QUEEN:
            self._num_queens += 1
            self._set_blocked_by_queen(row, col)
            print("num_queens = %d" % self._num_queens)
