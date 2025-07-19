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

import pytest
from Util import FatalException
from Cell import Cell, ALL_COLORS, BLUE, PINK, YELLOW


def test_ALL_COLORS():
    assert len(ALL_COLORS) == 10
    for c in ALL_COLORS:
        assert len(c) == 1
        assert c == c.upper()

def test_row():
    c = Cell(2, 3, BLUE)
    assert c.row() == 2

def test_col():
    c = Cell(5, 8, PINK)
    assert c.col() == 8

def test_color():
    c = Cell(0, 7, YELLOW)
    assert c.color() == 'Y'

def test_bad_color():
    with pytest.raises(FatalException):
        c = Cell(2, 4, 'A')
