from enum import Enum, unique
from random import choice


@unique
class SpaceInvadersFont(Enum):
    """
    Define font game.
    """
    LARGE = ('space_invaders', 50)
    MEDIUM = ('space_invaders', 25)
    SMALL = ('space_invaders', 20)


@unique
class SpaceInvadersColor(Enum):
    """
    Define font color.
    """
    WHITE = (255, 255, 255)
    GREEN = (78, 255, 87)
    YELLOW = (241, 255, 0)
    BLUE = (80, 255, 239)
    PURPLE = (203, 0, 255)
    RED = (237, 28, 36)


@unique
class SpaceInvadersSound(Enum):
    """
    Define sound key name.
    """
    SHOOT = 'shoot'
    SHOOT_2 = 'shoot2'
    INVADER_KILLED = 'invaderkilled'
    MYSTERY_ENTERED = 'mysteryentered'
    MYSTERY_KILLED = 'mysterykilled'
    SHIP_EXPLOSION = 'shipexplosion'


@unique
class SpaceInvadersMusic(Enum):
    """
    Define sound animation key name.
    """
    NOTE_0 = 'note_0'
    NOTE_1 = 'note_1'
    NOTE_2 = 'note_2'
    NOTE_3 = 'note_3'


@unique
class SpaceInvadersGfx(Enum):
    """
    Define gfx key
    """
    BACKGROUND = 'background'


@unique
class MoveDirection(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


DISPLAY_SIZE = (800, 600)

FPS = 60
TIME_PERIOD = 16

ENEMY_SIZE = (40, 35)
ENEMY_MOVE_TIME = 600
MYSTERY_MOVE_TIME = 25000
ENEMY_POSITION_DEFAULT = 65
ENEMY_POSITION_DELTA = 35
ENEMY_SHOUT_TIME_DELAY = 700
NO_ENEMY_DELAY = 1200
PLAYER_ALIVE_DELAY = 900

SOUND_SHOOT_VOLUME = 0.2
SOUND_ANIMATION_VOLUME = 0.5
SOUND_ANIMATION_TIME = ENEMY_MOVE_TIME
SOUND_MYSTERY_VOLUME = 0.3

PLAYER_LIFE = 3
PLAYER_CONTINUOUS_SHOOT = False

_SCORE = {0: 30,
          1: 20,
          2: 20,
          3: 10,
          4: 10}

MYSTERY_ROW = 5


def calculate_score_for_enemy(row: int) -> int:
    """
    Compute score for enemy row
    :param row: row index of enemy
    :return: a score
    """
    if row == 5:
        return choice([50, 100, 150, 300])
    return _SCORE[row]
