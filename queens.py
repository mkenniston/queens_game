#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2025 Michael S. Kenniston.  All rights reserved.

# Play the "Queens" game


import sys
from Game import Game
from Game import DISPLAY_COLOR


def main():
    args = sys.argv
    if len(args) != 1:
        raise BaseException("usage: %s" % args[0])
    with sys.stdin as file:
        description = file.read()

    game = Game(description)
    game.show(DISPLAY_COLOR)
    print()
    game.play()


if __name__ == '__main__':
    main()
