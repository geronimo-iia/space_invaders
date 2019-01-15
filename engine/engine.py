import sys
import pygame as pg

from .events import MUSIC_END


def initialize():
    """
    Initialize engine.
    """
    pg.mixer.pre_init(44100, -16, 2, 4096)
    pg.init()
    pg.font.init()
    pg.mixer.music.set_endevent(MUSIC_END)


def terminate(status: int = 0):
    """
    Quit engine.
    """
    pg.quit()
    sys.exit(status)
