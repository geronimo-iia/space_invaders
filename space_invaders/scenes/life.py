from engine import text, graphic, BasicSprite
from ..definition import *
from .base import BaseScene


class LifeScene(BaseScene):

    def __init__(self, game):
        BaseScene.__init__(self, game, active=True)
        self.life_text = BasicSprite(
            *text('Lives', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.SMALL.value, position=(640, 5)))
        self.life_1 = BasicSprite(*graphic('ship', position=(715, 3), scale=(23, 23)))
        self.life_2 = BasicSprite(*graphic('ship', position=(742, 3), scale=(23, 23)))
        self.life_3 = BasicSprite(*graphic('ship', position=(769, 3), scale=(23, 23)))

    def set_life(self, life):
        if life == 3:
            self.group.empty()
            self.group.add(self.life_text, self.life_1, self.life_2, self.life_3)
        elif life == 2:
            self.group.empty()
            self.group.add(self.life_text, self.life_1, self.life_2)
        elif life == 1:
            self.group.empty()
            self.group.add(self.life_text, self.life_1)
        elif life == 0:
            self.group.empty()
            self.group.add(self.life_text)

    def on_activate(self):
        self.set_life(self._game.life)

    def render(self):
        self.group.clear(self.screen, self.background)
        self.group.draw(self.screen)
        return True
