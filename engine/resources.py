"""
Resource Loader

Based on:
Sean J. McKiernan (Mekire)
https://github.com/Mekire/pygame-mutiscene-template-with-movie/blob/master/data/tools.py


"""
import os
import pygame as pg

_sfx_cache = {}
_gfx_cache = {}
_musics_cache = {}
_fonts_path_cache = {}
_fonts_cache = {}


def preload_resource(resource_directory=None):
    """
    Preload resource from specified directory or standard one if none is provided.
    :param resource_directory: resource directory (optional)
    :raise ValueError: if no resource directory can be found
    """
    directory = resource_directory if resource_directory else data_path()
    if directory is None:
        raise ValueError("resource directory not found")

    load_all_fonts(os.path.join(directory, 'fonts'))
    load_all_gfx(os.path.join(directory, 'graphics'))
    load_all_sfx(os.path.join(directory, 'sounds'))
    load_all_music(os.path.join(directory, 'musics'))


def get_sfx(name: str):
    global _sfx_cache
    return _sfx_cache.get(name)


def get_gfx(name: str):
    global _gfx_cache
    return _gfx_cache.get(name)


def get_music(name: str):
    global _musics_cache
    return _musics_cache.get(name)


def get_font(name: str, size: int):
    """
    Get specified font
    :param name: resource font name or system font name
    :param size: size
    :return: Font
    """
    global _fonts_path_cache
    global _fonts_cache

    key = name, size
    # lookup in cache
    font = _fonts_cache.get(key)
    if font is None:
        # make font
        font_path = _fonts_path_cache.get(name)
        try:
            if font_path:
                font = pg.font.Font(font_path, size)
            else:
                font = pg.font.SysFont(name, size)
        except Exception:
            font = pg.font.Font(None, size)
        # add font in cache
        _fonts_cache[key] = font
    return font


def data_path():
    for path in [os.path.join(os.getcwd(), 'data'),
                 os.path.join(os.path.dirname(__file__), '..', 'data')]:
        if os.path.exists(path):
            return path
    return None


def lookup_directory(directory: str, accept=None) -> [(str, str, str)]:
    """
    Lookup contains of directory
    :param directory: source directory
    :param accept: optional tuple of accepted extension
    :return: yield tuple of (name, suffix, file_path)
    """
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if accept is None or ext.lower() in accept:
                key = name.replace('/', '_').replace(' ', '').replace('\\', '').lower()
                file_path = os.path.join(root, filename)
                yield key, ext, file_path


def load_all_path(directory, accept) -> dict:
    """
    Create a dictionary of paths to files in given directory if their extensions are in accept.
    :param directory: root directory
    :param accept: tuple of accepted extension
    :return: a dictionary of name, path
    """
    paths = {}
    if os.path.exists(directory):
        for song in os.listdir(directory):
            name, ext = os.path.splitext(song)
            if ext.lower() in accept:
                paths[name.lower()] = os.path.join(directory, song)
    return paths


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Create a dictionary of paths to music files in given directory
    if their extensions are in accept.
    :param directory: music root directory
    :param accept: tuple of accepted extension, (".wav", ".mp3", ".ogg", ".mdi") per default
    :return: a dictionary of name, path
    """
    global _musics_cache
    _musics_cache = load_all_path(directory, accept)


def load_all_fonts(directory, accept=(".ttf",)):
    """
    Create a dictionary of paths to font files in given directory
    if their extensions are in accept.
    :param directory: fonts directory
    :param accept: tuple of accepted extension, (".ttf",) per default
    :return: a dictionary of name, path
    """
    global _fonts_path_cache
    _fonts_path_cache = load_all_path(directory, accept)


def load_all_gfx(directory, color_key=None, accept=(".png", ".jpg", ".bmp")):
    """
    Load all graphics with extensions in the accept argument.
    If alpha transparency is found in the image the image will be converted using
    convert_alpha().
    If no alpha transparency is detected image will be converted using convert() and colorkey will be set to color_key if provided.
    
    :param directory: graphics directory path
    :param color_key: optional color_key
    :param accept: tuple of accepted extension, (".png", ".jpg", ".bmp") per default
    :return: a dictionary of name, image
    """
    global _gfx_cache
    _gfx_cache = {}
    if os.path.exists(directory):
        for pic in os.listdir(directory):
            name, ext = os.path.splitext(pic)
            if ext.lower() in accept:
                img = pg.image.load(os.path.join(directory, pic))
                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                    if color_key:
                        img.set_colorkey(color_key)
                _gfx_cache[name.lower()] = img


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Load all sfx of extensions found in accept.
    :param directory: sounds directiry
    :param accept: tuple of accepted extension, (".wav", ".mp3", ".ogg", ".mdi") per default
    :return: a dictionary of name, Sound
    """
    global _sfx_cache
    _sfx_cache = {}
    if os.path.exists(directory):
        for fx in os.listdir(directory):
            name, ext = os.path.splitext(fx)
            if ext.lower() in accept:
                try:
                    _sfx_cache[name] = pg.mixer.Sound(os.path.join(directory, fx))
                except _:
                    pass
