from pygame import transform, time

from engine import text, graphic, BasicSprite

from ..definition import SpaceInvadersColor, SpaceInvadersFont, MYSTERY_ROW

_IMG_COLORS = ['purple', 'blue', 'blue', 'green', 'green']


class MysteryExplosion(BasicSprite):

    def __init__(self, score, position):
        x, y = position
        surface, rect = text(str(score), SpaceInvadersColor.WHITE.value, *SpaceInvadersFont.SMALL.value,
                             position=(x + 20, y + 6))
        BasicSprite.__init__(self, surface, rect)
        self.start_time = 600
        self.row = MYSTERY_ROW

    def update(self, dt):
        self.start_time -= dt
        if self.start_time <= 0:
            self.kill()


class ShipExplosion(BasicSprite):

    def __init__(self, position):
        surface, rect = graphic('ship', position)
        BasicSprite.__init__(self, surface, rect)
        self.start_time = 900

    def update(self, dt):
        self.start_time -= dt
        if self.start_time <= 0:
            self.kill()


class EnemyExplosion(BasicSprite):

    def __init__(self, row, position):
        surface, rect = graphic(f'explosion{_IMG_COLORS[row]}', position)
        surface = transform.scale(surface, (40, 35))
        BasicSprite.__init__(self, surface, rect)
        self.start_time = 0
        self.row = row
        self.moved = False

    def update(self, dt):
        self.start_time += dt
        if 100 < self.start_time <= 200:
            if not self.moved:
                self.image = transform.scale(self.image, (50, 45))
                self.rect.x -= 6
                self.rect.y -= 6
                self.moved = True
        elif self.start_time > 400:
            self.kill()
