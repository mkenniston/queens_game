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

# Define the state of the game for the "Queens" game,
# and provide the logic about how to play.


from Geometry import Geometry
from State import State, FREE, BLOCKED, QUEEN

DISPLAY_STATE = "state"
DISPLAY_COLOR = "color"


class Game():
    def __init__(self, description):
        self._geom = Geometry(description)
        self._size = self._geom.size()
        self._state = State(self._geom)
        self.show(self._state, DISPLAY_COLOR)

    def _show_horiz_line(self):
        pieces = ['+']
        for col in range(self._size):
            pieces.append('---+')
        print("".join(pieces))

    def _show_horiz_info(self, state, row, which):
        pieces = ['|']
        for col in range(self._size):
            pieces.append(' ')
            if which == DISPLAY_COLOR:
                info = state.geom().cell_color(row, col)
            else:
                info = state.cell_state(row, col)
            pieces.append(info)
            pieces.append(' |')
        print("".join(pieces))
        self._show_horiz_line()

    def show(self, state, which):
        self._show_horiz_line()
        for row in range(self._size):
            self._show_horiz_info(state, row, which)
        print()

    def play(self):
        rv = self._solve(self._state)
        if rv:
            print("The game is won!")

    def _solve(self, state):
        while True:
            state.recalc_free_cells()
            self.show(state, DISPLAY_STATE)

            if state.num_queens() == self._size:
                return True

            if self._add_a_queen(state):
                continue
            if self._reserve_linear_free_space(state):
                continue

            return self._try_guesses(state)

    def _try_guesses(self, state):
        # Sort groups by number of free cells
        groups = state.geom().groups()
        sort_by_num_free = (
            lambda x: state.num_free_cells_in_group(x.number()))
        sorted_groups = sorted(groups, key=sort_by_num_free)
        for group in sorted_groups:
            free_cells = state.free_cells_in_group(group.number())
            num_free_cells = len(free_cells)
            if num_free_cells > 0:
                print("looking at group %s with %d free" %
                      (group.name(), num_free_cells))
                for queen in free_cells:
                    qr = queen.row()
                    qc = queen.col()
                    trial_state = State(state)
                    print("making a guess: try a queen at %d, %d" % (qr, qc))
                    print("TRACE A: %s" % trial_state.cell_state(qr, qc))
                    trial_state.set_cell_state(qr, qc, QUEEN)
                    print("TRACE B: %s" % trial_state.cell_state(qr, qc))
                    if self._solve(trial_state):
                        return True
                    print("retracting guess at %d, %d" % (qr, qc))
                    state.set_cell_state(qr, qc, BLOCKED)
        return False

    # Look for a group which has exactly one free cell.
    # A queen must go there (for rows, columns, and color groups).

    def _add_a_queen(self, state):
        geom = state.geom()
        for group in geom.groups():
            free_cells = state.get_cells_in_group(group, state=FREE)
            if len(free_cells) == 1:
                cell = free_cells[0]
                state.set_cell_state(cell.row(), cell.col(), QUEEN)
                print("group %s has only one free cell,"
                      " put a Queen at (%d, %d)" % (
                       group.name(), cell.row(), cell.col()))
                return True
        return False

    # Look for a group whose free cells are all in one row or column.
    # The Queen must go in one of those, so block all cells
    # in that row or column that belong to other groups.

    def _reserve_linear_free_space(self, state):
        geom = state.geom()
        for color_group in geom.color_groups():
            free_cells = state.get_cells_in_group(
                             color_group, state=FREE)
            free_rows = set()
            free_cols = set()
            for cell in free_cells:
                free_rows.add(cell.row())
                free_cols.add(cell.col())

            if len(free_rows) == 1:
                row_number = free_rows.pop()
                line_cells = geom.row_group(row_number).cells()
                if self._reserve_strip(state, free_cells, line_cells):
                    print("all group %s free cells are in row %d, "
                          " block the rest of the row" %
                          (color_group.name(), cell.row()))
                    return True

            if len(free_cols) == 1:
                col_number = free_cols.pop()
                line_cells = geom.col_group(col_number).cells()
                if self._reserve_strip(state, free_cells, line_cells):
                    print("all group %s free cells are in col %d, "
                          " block the rest of the col" %
                          (color_group.name(), cell.col()))
                    return True

        return False

    def _reserve_strip(self, bs, free_cells, line_cells):
        changed = False
        for line_cell in line_cells:
            row = line_cell.row()
            col = line_cell.col()
            if (line_cell not in free_cells and
                    bs.cell_state(row, col) != BLOCKED):
                bs.set_cell_state(row, col, BLOCKED)
                changed = True
        return changed
