import pygame as pg

from engine import text, graphic, BasicSprite
from ..definition import SpaceInvadersFont, SpaceInvadersColor
from .base import BaseScene


class MainMenuScene(BaseScene):

    def __init__(self, game):
        BaseScene.__init__(self, game, active=True)
        items = [
            text('Space Invaders', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.LARGE.value, position=(164, 155)),
            text('Press any key to continue', SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.MEDIUM.value,
                 position=(201, 225)),
            graphic('enemy3_1', (318, 370), (40, 40)),
            text('   =   10 pts', SpaceInvadersColor.GREEN.value, *SpaceInvadersFont.MEDIUM.value, position=(368, 270)),
            graphic('enemy2_2', (318, 320), (40, 40)),
            text('   =   20 pts', SpaceInvadersColor.BLUE.value, *SpaceInvadersFont.MEDIUM.value, position=(368, 320)),
            graphic('enemy1_2', (318, 270), (40, 40)),
            text('   =   30 pts', SpaceInvadersColor.PURPLE.value, *SpaceInvadersFont.MEDIUM.value,
                 position=(368, 370)),
            graphic('mystery', (299, 420), (80, 40)),
            text('   =  ?????', SpaceInvadersColor.RED.value, *SpaceInvadersFont.MEDIUM.value, position=(368, 420))
        ]
        for item in items:
            self.group.add(BasicSprite(*item))

    def handle_event(self, event):
        if event.type == pg.KEYUP:
            self._game.start_new_game()
            return False
