from pygame.sprite import Sprite
from pygame import transform, time

from engine import get_gfx, get_sfx

from ..definition import SpaceInvadersSound, SOUND_MYSTERY_VOLUME, MYSTERY_MOVE_TIME


class Mystery(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = transform.scale(get_gfx('mystery'), (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.move_time = MYSTERY_MOVE_TIME
        self.direction = 1
        self.timer = time.get_ticks()
        self.mystery_entered = get_sfx(SpaceInvadersSound.MYSTERY_ENTERED.value)
        self.mystery_entered.set_volume(SOUND_MYSTERY_VOLUME)
        self.play_sound = True

    def update(self, dt):
        reset_timer = False
        self.move_time -= dt
        if self.move_time <= 0:
            if (self.rect.x < 0 or self.rect.x > 800) and self.play_sound:
                self.mystery_entered.play()
                self.play_sound = False
            if self.rect.x < 840 and self.direction == 1:
                self.mystery_entered.fadeout(4000)
                self.rect.x += 2
            if self.rect.x > -100 and self.direction == -1:
                self.mystery_entered.fadeout(4000)
                self.rect.x -= 2
        if self.rect.x > 830:
            self.play_sound = True
            self.direction = -1
            reset_timer = True
        if self.rect.x < -90:
            self.play_sound = True
            self.direction = 1
            reset_timer = True
        if self.move_time <= 0 and reset_timer:
            self.move_time = MYSTERY_MOVE_TIME
