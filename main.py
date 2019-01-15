#!/usr/bin/env python

# Space Invaders
# Created by Jerome Guibert
#
from engine import *
from space_invaders import *

if __name__ == '__main__':
    try:
        initialize()
        screen = create_display('Hello', *DISPLAY_SIZE)
        preload_resource()
        game = SpaceInvadersGame(screen=screen, fps=FPS)
        game.main()
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')
    terminate(0)
