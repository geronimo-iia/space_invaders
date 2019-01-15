from pygame.sprite import Sprite

from engine import graphic
from ..definition import TIME_PERIOD


class Bullet(Sprite):

    def __init__(self, position, direction, speed, filename, side):
        Sprite.__init__(self)
        self.image, self.rect = graphic(filename, position=position)
        self.speed = speed
        self.direction = direction
        self.side = side

    def update(self, dt, *args):
        # TODO add delta_time
        self.rect.y += (self.speed * self.direction * dt / TIME_PERIOD)
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()
