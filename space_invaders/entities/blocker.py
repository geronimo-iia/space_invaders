from pygame.sprite import Sprite, Group
from pygame import Surface

from ..definition import SpaceInvadersColor


class Blocker(Sprite):
    def __init__(self, size, color: SpaceInvadersColor, row, column):
        Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color.value
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column


def _build_blockers(number) -> Group:
    blocker_group = Group()
    for row in range(4):
        for column in range(9):
            blocker = Blocker(10, SpaceInvadersColor.GREEN, row, column)
            blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
            blocker.rect.y = 450 + (row * blocker.height)
            blocker_group.add(blocker)
    return blocker_group


def build_blockers_group() -> Group:
    return Group(_build_blockers(0), _build_blockers(1), _build_blockers(2), _build_blockers(3))
