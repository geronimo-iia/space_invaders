import pygame as pg
from engine import *
from .scenes import *
from .definition import PLAYER_LIFE


class SpaceInvadersGame(GameScene):

    def __init__(self, screen, fps):
        GameScene.__init__(self, screen, fps)
        self.main_screen = None
        self.game_round = None
        self.next_round = None
        self.game_over = None

        self.life_scene = None
        self.score_scene = None

        self.score = 0
        self.life = PLAYER_LIFE
        self.new_game = True

    def on_start(self):
        self.main_screen = MainMenuScene(self)
        self.scenes.append(self.main_screen)

        self.next_round = NextRoundScene(self)
        self.scenes.append(self.next_round)

        self.game_over = GameOverScene(self)
        self.scenes.append(self.game_over)

        self.game_round = GameRound(self)
        self.scenes.append(self.game_round)

        self.life_scene = LifeScene(self)
        self.scenes.append(self.life_scene)

        self.score_scene = ScoreScene(self)
        self.scenes.append(self.score_scene)

        # initial state
        self.show_main_menu()

    def handle_event(self, event):
        # handle Escape key
        if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            self.running = False
            return
        super().handle_event(event)

    def start_new_game(self):
        self.set_score(0)
        self.set_life(PLAYER_LIFE)
        self.new_game = True
        self.main_screen.disable()
        self.next_round.disable()
        self.life_scene.activate()
        self.score_scene.activate()
        self.game_round.activate()

    def start_next_round(self):
        if self.life < PLAYER_LIFE:
            self.life += 1
        self.new_game = False
        self.next_round.disable()
        self.life_scene.activate()
        self.score_scene.activate()
        self.game_round.activate()

    def show_game_over(self):
        self.game_round.disable()
        self.game_over.activate()

    def show_main_menu(self):
        self.enable_only(self.main_screen)

    def show_next_round(self):
        self.enable_only(self.next_round)

    def set_score(self, new_score: int):
        self.score = new_score
        self.score_scene.set_score(self.score)

    def set_life(self, new_life):
        self.life = new_life
        self.life_scene.set_life(self.life)
