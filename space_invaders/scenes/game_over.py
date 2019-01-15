from engine import text, BasicSprite
from ..definition import SpaceInvadersFont, SpaceInvadersColor

from .base import BaseScene


class GameOverScene(BaseScene):
    """
    Show Next Round Message.
    """

    def __init__(self, game):
        BaseScene.__init__(self, game)
        self.group.add(BasicSprite(
            *text('Game Over', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.LARGE.value, position=(250, 270))))
        self.menu_time = 0.0

    def on_activate(self):
        super().on_activate()
        self.menu_time = 3000

    def update(self, dt):
        self.menu_time -= dt
        if self.menu_time <= 0:
            self._game.show_main_menu()
        return False
