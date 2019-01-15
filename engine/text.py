"""
Text helper
"""
from .resources import get_font


def text(message: str, color, name: str, size: int, position):
    message = message if message else ''
    font = get_font(name, size)
    surface = font.render(message, True, color)
    return surface, surface.get_rect(topleft=position)
