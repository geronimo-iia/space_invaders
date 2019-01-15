from pygame.sprite import Sprite
from engine import get_gfx
from ..definition import MoveDirection, TIME_PERIOD


class Ship(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = get_gfx('ship')
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5
        self._move = MoveDirection.NONE

    def update(self, dt):
        if self._move == MoveDirection.LEFT and self.rect.x > 10:
            self.rect.x -= (self.speed * dt / TIME_PERIOD)
        elif self._move == MoveDirection.RIGHT and self.rect.x < 740:
            self.rect.x += (self.speed * dt / TIME_PERIOD)

    def move(self, direction: MoveDirection):
        self._move = direction
