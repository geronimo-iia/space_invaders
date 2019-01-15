from engine import text, BasicSprite
from ..definition import SpaceInvadersFont, SpaceInvadersColor
from .base import BaseScene


class NextRoundScene(BaseScene):
    """
    Show Next Round Message.
    """

    def __init__(self, game):
        BaseScene.__init__(self, game)
        self.group.add(BasicSprite(
            *text('Next Round', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.LARGE.value, position=(240, 270))))
        self.menu_time = None

    def on_activate(self):
        super().on_activate()
        self.menu_time = 900

    def update(self, dt):
        self.menu_time -= dt
        if self.menu_time <= 0:
            self._game.start_next_round()
        return False
