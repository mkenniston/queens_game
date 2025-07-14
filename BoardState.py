#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2025 Michael S. Kenniston.  All rights reserved.

# Define the current state of a "Queens" game
# The "BoardState" object contains all the mutable information.


FREE = ' '
BLOCKED = 'x'
QUEEN = 'Q'
ALL_STATES = [FREE, BLOCKED, QUEEN]


class BoardState():
    def __init__(self, board_geom):
        self._board_geom = board_geom
        self._groups = board_geom.groups()
        size = board_geom.size()
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
