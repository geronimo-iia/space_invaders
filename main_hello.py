#!/usr/bin/env python

# Space Invaders
# Created by Jerome Guibert
#
from engine import *

if __name__ == '__main__':
    try:
        initialize()
        screen = create_display('Hello', width=800, height=600)
        preload_resource()
        game = GameScene(screen=screen)
        game.main()
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')
    terminate(0)
