import pygame as pg

from engine import get_gfx, Scene
from ..definition import SpaceInvadersGfx


class BaseScene(Scene):

    def __init__(self, game, screen=None, active: bool = False):
        Scene.__init__(self, game, screen, active)
        self.group = pg.sprite.Group()
        self.background = get_gfx(SpaceInvadersGfx.BACKGROUND.value)
        self._first_rendering = True

    def on_activate(self):
        self._first_rendering = True

    def render(self):
        if self._first_rendering:
            self._first_rendering = False
            self.screen.blit(self.background, (0, 0))
        self.group.clear(self.screen, self.background)
        self.group.draw(self.screen)
        return True
