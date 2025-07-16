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


from BoardGeom import BoardGeom
from BoardState import BoardState, FREE, BLOCKED, QUEEN

DISPLAY_STATE = "state"
DISPLAY_COLOR = "color"


class Game():
    def __init__(self, description):
        self._board_geom = BoardGeom(description)
        self._size = self._board_geom.size()
        self._board_state = BoardState(self._board_geom)

    def _show_horiz_line(self):
        pieces = ['+']
        for col in range(self._size):
            pieces.append('---+')
        print("".join(pieces))

    def _show_horiz_info(self, row, which):
        pieces = ['|']
        for col in range(self._size):
            pieces.append(' ')
            if which == DISPLAY_COLOR:
                info = self._board_geom.cell_color(row, col)
            else:
                info = self._board_state.cell_state(row, col)
            pieces.append(info)
            pieces.append(' |')
        print("".join(pieces))
        self._show_horiz_line()

    def show(self, which):
        self._show_horiz_line()
        for row in range(self._size):
            self._show_horiz_info(row, which)

    def play(self):
        self._solve(self._board_state)

    def _solve(self, board_state):
        while True:
            self.show(DISPLAY_STATE)
            print()

            if self._board_state.num_queens() == self._size:
                print("The game is won!")
                return

            if self._add_a_queen():
                continue
            if self._reserve_linear_free_space():
                continue

            break
        print("no more moves found")

    # Look for a group which has exactly one free cell.
    # A queen must go there (for rows, columns, and color groups).

    def _add_a_queen(self):
        bs = self._board_state
        for group in self._board_geom.groups():
            free_cells = bs.get_cells_in_group(group, state=FREE)
            if len(free_cells) == 1:
                cell = free_cells[0]
                self._board_state.set_cell_state(cell.row(), cell.col(), QUEEN)
                print("group %s has only one free cell,"
                      " put a Queen at (%d, %d)" % (
                       group.name(), cell.row(), cell.col()))
                return True
        return False

    # Look for a group whose free cells are all in one row or column.
    # The Queen must go in one of those, so block all other cells
    # in that row or column.

    def _reserve_linear_free_space(self):
        bs = self._board_state
        bg = bs._board_geom
        for color_group in bg.color_groups():
            free_cells = bs.get_cells_in_group(color_group, state=FREE)
            free_rows = set()
            free_cols = set()
            for cell in free_cells:
                free_rows.add(cell.row())
                free_cols.add(cell.col())

            if len(free_rows) == 1:
                row_number = free_rows.pop()
                line_cells = bg.row_group(row_number).cells()
                if self._reserve_strip(bs, free_cells, line_cells):
                    print("group %s has all free cells in row %d, "
                          " block the rest of the row" %
                          (color_group.name(), cell.row()))
                    return True

            if len(free_cols) == 1:
                col_number = free_cols.pop()
                line_cells = bg.col_group(col_number).cells()
                if self._reserve_strip(bs, free_cells, line_cells):
                    print("group %s has all free cells in col %d, "
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
