from pygame import transform as _transform
from .resources import get_gfx


def graphic(image_name: str, position=None, scale=None):
    surface = get_gfx(image_name)
    if scale:
        surface = _transform.scale(surface, scale)
    if position:
        rect = surface.get_rect(topleft=position)
    else:
        rect = surface.get_rect()
    return surface, rect
