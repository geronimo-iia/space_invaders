"""
Define game scene
"""
import pygame as pg

from engine import get_sfx, SoundSequence
from ..definition import *
from .base import BaseScene
from ..entities import *


class GameRound(BaseScene):

    def __init__(self, game):
        BaseScene.__init__(self, game, active=True)
        self.start_time = 0.0
        self.game_over = False

        self.player_group = pg.sprite.Group()
        self.player_bullets_group = pg.sprite.Group()
        self.enemy_bullets_group = pg.sprite.Group()
        self.explosions_group = pg.sprite.Group()
        self.mystery_group = pg.sprite.Group()

        self.blockers_group = None

        self.player = None
        self.player_alive = False
        self.player_alive_time = PLAYER_ALIVE_DELAY
        self.player_shoot = False

        self.enemies_group = None
        self.enemies_shoot_time = ENEMY_SHOUT_TIME_DELAY
        self.enemies_dead_time = 0.0

        # Counter for enemy starting position (increased each new round)
        self.enemy_position_start = ENEMY_POSITION_DEFAULT
        # Current enemy starting position
        self.enemy_position = self.enemy_position_start

        # sounds
        self.sfx_shoot = get_sfx(SpaceInvadersSound.SHOOT.value)
        self.sfx_shoot.set_volume(SOUND_SHOOT_VOLUME)
        self.sfx_shoot_2 = get_sfx(SpaceInvadersSound.SHOOT_2.value)
        self.sfx_shoot_2.set_volume(SOUND_SHOOT_VOLUME)
        self.sfx_ship_explosion = get_sfx(SpaceInvadersSound.SHIP_EXPLOSION.value)
        self.sfx_ship_explosion.set_volume(SOUND_SHOOT_VOLUME)
        self.sfx_mystery_killed = get_sfx(SpaceInvadersSound.MYSTERY_KILLED.value)
        self.sfx_mystery_killed.set_volume(SOUND_SHOOT_VOLUME)
        self.sfx_invader_killed = get_sfx(SpaceInvadersSound.INVADER_KILLED.value)
        self.sfx_invader_killed.set_volume(SOUND_SHOOT_VOLUME)

        notes = []
        for sound_name in SpaceInvadersMusic:
            sound = get_sfx(sound_name.value)
            sound.set_volume(SOUND_ANIMATION_VOLUME)
            notes.append(sound)
        self.sfx_animation = SoundSequence(duration_time=SOUND_ANIMATION_TIME, running=False, sounds=notes)

    def on_activate(self):
        super().on_activate()
        if self._game.new_game:
            self.blockers_group = build_blockers_group()
            self.group.add(self.blockers_group)
            self.enemy_position_start = ENEMY_POSITION_DEFAULT
        else:
            self.enemy_position_start += ENEMY_POSITION_DELTA
            # max position
            if self.enemy_position_start > (ENEMY_POSITION_DEFAULT + 6 * ENEMY_POSITION_DELTA):
                self.enemy_position_start = ENEMY_POSITION_DEFAULT

        self.game_over = False
        self.start_time = pg.time.get_ticks()
        self.enemies_shoot_time = ENEMY_SHOUT_TIME_DELAY
        self.enemies_dead_time = 0.0

        self.enemy_position = self.enemy_position_start

        self.group.empty()
        Mystery().add(self.mystery_group, self.group)
        self.enemies_group = build_enemies_group(self.enemy_position, 10, 5)
        self.enemies_group.set_speed_listener(self.enemies_speed_listener)
        self.player_alive = False
        self.new_player()
        self.group.add(self.blockers_group, self.enemies_group, self.explosions_group)

        self.sfx_animation.set_duration(SOUND_ANIMATION_TIME)
        self.sfx_animation.start()

    def enemies_speed_listener(self, speed):
        self.sfx_animation.set_duration(speed)

    def on_disabled(self):
        self.sfx_animation.stop()
        self.group.empty()

        self.player_group.empty()
        self.player_bullets_group.empty()
        if self.enemies_group:
            self.enemies_group.empty()
        self.enemies_group = None
        self.enemy_bullets_group.empty()
        self.explosions_group.empty()
        self.mystery_group.empty()

    def handle_event(self, event):
        # manage player control
        if self.player_alive:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(MoveDirection.LEFT)
                elif event.key == pg.K_RIGHT:
                    self.player.move(MoveDirection.RIGHT)
                elif event.key == pg.K_SPACE:
                    self.player_shoot = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    self.player.move(MoveDirection.NONE)
                elif event.key == pg.K_SPACE:
                    self.player_shoot = False
        return True

    def update(self, dt):
        # sounds animation
        self.sfx_animation.update(dt)
        # live player
        self.player_update(dt)
        # no more enemies
        if len(self.enemies_group) == 0:
            self.sfx_animation.stop()  # stop sound enemy animation
            # wait NO_ENEMY_DELAY before next round
            self.enemies_dead_time += dt
            if self.enemies_dead_time >= NO_ENEMY_DELAY:
                self._game.show_next_round()
            return
        self.enemies_shoot_update(dt)
        self.group.update(dt)
        # ths call is not done since group.update (?)
        self.enemies_group.update(dt)
        self.check_collisions()
        if self.game_over:
            self._game.show_game_over()
        return True

    def calculate_score(self, row):
        _score = calculate_score_for_enemy(row)
        self._game.set_score(self._game.score + _score)
        return _score

    def kill_player(self):
        """
        Kill current player
        """
        if self.player_alive:
            self.sfx_ship_explosion.play()
            ShipExplosion((self.player.rect.x, self.player.rect.y)).add(self.explosions_group, self.group)
            # self.player.remove(self.group, self.player_group)
            self.player.kill()
            self.player_alive = False
            self.player_alive_time = PLAYER_ALIVE_DELAY

            life = self._game.life
            if life > 0:
                life -= 1
                self._game.set_life(life)
            elif life == 0:
                self.game_over = True

    def new_player(self):
        """
        Build a new player
        """
        if not self.player_alive:
            self.player = Ship()
            self.player.add(self.player_group, self.group)
            self.player_alive = True
            self.player_alive_time = PLAYER_ALIVE_DELAY
            self.player_shoot = False

    def player_update(self, dt: float):
        """
        Manage player alive and shoot
        """
        if not self.player_alive:
            # wait PLAYER_ALIVE_DELAY before new player
            self.player_alive_time -= dt
            if self.player_alive_time < 0:
                self.new_player()
        elif self.player_shoot and len(self.player_bullets_group) == 0:
            if not PLAYER_CONTINUOUS_SHOOT:
                self.player_shoot = False
            if self._game.score < 1000:
                Bullet((self.player.rect.x + 23, self.player.rect.y + 5), -1, 15, 'laser', 'center').add(
                    self.player_bullets_group, self.group)
                self.sfx_shoot.play()
            else:
                Bullet((self.player.rect.x + 8, self.player.rect.y + 5), -1, 15, 'laser', 'left').add(
                    self.player_bullets_group, self.group)
                Bullet((self.player.rect.x + 38, self.player.rect.y + 5), -1, 15, 'laser', 'right').add(
                    self.player_bullets_group, self.group)
                self.sfx_shoot_2.play()

    def enemies_shoot_update(self, dt: float):
        """
        Manage enemies shoot
        """
        self.enemies_shoot_time -= dt
        if self.enemies_shoot_time <= 0:
            self.enemies_shoot_time = ENEMY_SHOUT_TIME_DELAY
            enemy = self.enemies_group.random_bottom()
            if enemy:
                Bullet((enemy.rect.x + 14, enemy.rect.y + 20), 1, 5, 'enemylaser', 'center').add(
                    self.enemy_bullets_group, self.group)

    def check_collisions(self):
        # player bullet and enemy bullet collide
        collide_dict = pg.sprite.groupcollide(self.player_bullets_group, self.enemy_bullets_group, True, False)
        if collide_dict:
            for value in collide_dict.values():
                for current_sprite in value:
                    current_sprite.remove(self.enemy_bullets_group, self.group)

        # enemies and player bullet collide
        enemies_dict = pg.sprite.groupcollide(self.player_bullets_group, self.enemies_group, True, False)
        if enemies_dict:
            for value in enemies_dict.values():
                for current_sprite in value:
                    self.enemies_group.kill(current_sprite)
                    self.sfx_invader_killed.play()
                    self.calculate_score(current_sprite.row)
                    EnemyExplosion(current_sprite.row, (current_sprite.rect.x, current_sprite.rect.y)).add(
                        self.explosions_group, self.group)
                    self.enemies_group.remove(current_sprite)
                    break

        mystery_dict = pg.sprite.groupcollide(self.player_bullets_group, self.mystery_group, True, True)
        if mystery_dict:
            for value in mystery_dict.values():
                for current_sprite in value:
                    current_sprite.mystery_entered.stop()
                    self.sfx_mystery_killed.play()
                    score = self.calculate_score(current_sprite.row)
                    MysteryExplosion(score, (current_sprite.rect.x, current_sprite.rect.y)).add(self.explosions_group,
                                                                                                self.group)
                    current_sprite.remove(self.mystery_group, self.group)
                    Mystery().add(self.mystery_group, self.group)
                    break

        bullets_dict = pg.sprite.groupcollide(self.enemy_bullets_group, self.player_group, True, False)
        if bullets_dict:
            if len(bullets_dict) > 0:
                self.kill_player()

        if pg.sprite.groupcollide(self.enemies_group, self.player_group, True, True):
            self.game_over = True

        pg.sprite.groupcollide(self.player_bullets_group, self.blockers_group, True, True)
        pg.sprite.groupcollide(self.enemy_bullets_group, self.blockers_group, True, True)
        pg.sprite.groupcollide(self.enemies_group, self.blockers_group, False, True)
