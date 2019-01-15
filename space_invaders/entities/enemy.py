from pygame.sprite import Sprite
from pygame import transform
from engine import get_gfx

from ..definition import ENEMY_SIZE

_IMAGES = {0: ['1_2', '1_1'],
           1: ['2_2', '2_1'],
           2: ['2_2', '2_1'],
           3: ['3_1', '3_2'],
           4: ['3_1', '3_2'],
           }


class Enemy(Sprite):
    def __init__(self, row, column, images):
        Sprite.__init__(self)
        self.row: int = row
        self.column: int = column
        self.images = images
        self.index: int = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


def build_enemy(row: int, column: int, scale=ENEMY_SIZE):
    images = list(
        map(lambda img_num: transform.scale(get_gfx(f'enemy{img_num}'), scale), _IMAGES[row]))
    return Enemy(row, column, images)
