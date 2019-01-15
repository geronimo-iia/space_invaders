import pygame as pg


def create_display(caption, width, height, flags=0):
    """
    Initialize a window or screen for display.
    :param caption: window caption
    :param width: display width
    :param height: display height
    :param flags: optional display flag (see https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)
    :return:
    """
    screen = pg.display.set_mode((width, height), flags)
    pg.display.set_caption(caption)
    return screen
