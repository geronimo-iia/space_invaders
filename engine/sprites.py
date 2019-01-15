from pygame.sprite import Sprite


class BasicSprite(Sprite):
    """
    Define a basic sprite composed of a surface and rect.
    """
    def __init__(self, surface, rect):
        Sprite.__init__(self)
        self.image = surface
        self.rect = rect

    def set_position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
