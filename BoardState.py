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
# The "BoardState" object contains all the mutable information.


from BoardGeom import BoardGeom

FREE = ' '
BLOCKED = 'x'
QUEEN = 'Q'
ALL_STATES = [FREE, BLOCKED, QUEEN]


class BoardState():
    def __init__(self, arg):
        if isinstance(arg, BoardGeom):
            self._init_new(arg)
        elif isinstance(arg, BoardState):
            self._init_copy(arg)
        else:
            raise BaseException("illegal arg type %s" % type(arg))
        pass
        return

    def _init_copy(self, new_copy):
        new_copy._board_geom = self._board_geom
        new_copy._groups = self._groups
        size = self._board_geom.size()
        self._cell_states = []
        for row in range(size):
            one_row = []
            for col in range(size):
                one_row.append(self._cell_states[row][col])
            new_copy._cell_states.append(one_row)
        new_copy.recalc_free_cells()
        new_copy._num_queens = self._num_queens

    def _init_new(self, board_geom):
        self._board_geom = board_geom
        self._groups = self._board_geom.groups()
        size = self._board_geom.size()
        self._cell_states = [[FREE] * size for i in range(size)]
        self.recalc_free_cells()
        self._num_queens = 0

    def board_geom(self):
        return self._board_geom

    def num_queens(self):
        return self._num_queens

    def recalc_free_cells(self):
        self._free_cells = []
        for g in self._groups:
            self._free_cells.append(self.get_cells_in_group(g, state=FREE))

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

    def num_free_in_group(self, group_number):
        return len(self._free_cells[group_number])

    def get_cell_state(self, row, col):
        return self._cell_states[row][col]

    def set_cell_state(self, row, col, new_state):
        size = self._board_geom.size()
        if row < 0 or row >= size or col < 0 or col >= size:
            return  # make it easier to block cells adjacent to new queen
        if new_state not in ALL_STATES:
            raise BaseException("illegal state %s" % new_state)
        old_state = self._cell_states[row][col]
        if new_state == old_state:
            return  # harmless no-op
        if old_state == BLOCKED:
            raise BaseException("attempt to unblock (%d, %d)" % (row, col))
        if old_state == QUEEN:
            raise BaseException("attempt to unqueen (%d, %d)" % (row, col))

        self._cell_states[row][col] = new_state
        if new_state == QUEEN:
            for row_inc in [-1, 0, +1]:
                for col_inc in [-1, 0, +1]:
                    if row_inc == 0 and col_inc == 0:
                        continue
                    self.set_cell_state(row + row_inc, col + col_inc, BLOCKED)
            for r in range(size):
                if r != row:
                    self.set_cell_state(r, col, BLOCKED)
            for c in range(size):
                if c != col:
                    self.set_cell_state(row, c, BLOCKED)
            self._num_queens += 1
