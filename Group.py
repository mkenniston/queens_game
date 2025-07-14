#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2025 Michael S. Kenniston.  All rights reserved.

# Define groups of cells for the "Queens" game


class Group():
    def __init__(self, board_geom, number, name):
        self._board_geom = board_geom
        self._number = number
        self._name = name
        self._cells = []

    def number(self):
        return self._number

    def name(self):
        return self._name

    def add(self, cell):
        self._cells.append(cell)

    def cells(self):
        return self._cells


class RowGroup(Group):
    pass


class ColGroup(Group):
    pass


class ColorGroup(Group):
    pass
