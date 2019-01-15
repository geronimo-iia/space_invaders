from engine import text, BasicSprite
from ..definition import *
from .base import BaseScene


class ScoreScene(BaseScene):

    def __init__(self, game):
        BaseScene.__init__(self, game, active=True)
        self.score_label = BasicSprite(
            *text('Score', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.SMALL.value, position=(5, 5)))

    def on_activate(self):
        self.set_score(self._game.score)

    def set_score(self, score):
        self.group.empty()
        self.group.add(self.score_label)
        self.group.add(
            BasicSprite(
                *text(str(score), SpaceInvadersColor.GREEN.value, *SpaceInvadersFont.SMALL.value, position=(85, 5))))
