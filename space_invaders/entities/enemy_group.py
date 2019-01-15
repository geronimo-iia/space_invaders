from pygame.sprite import Group
from random import randint
from typing import Optional, List, Callable
from .enemy import Enemy, build_enemy
from ..definition import ENEMY_MOVE_TIME


class EnemiesGroup(Group):

    def __init__(self, columns, rows):
        Group.__init__(self)
        self.enemies: List[List[Optional[Enemy]]] = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.left_add_move = 0
        self.rightAddMove = 0
        self.move_time = ENEMY_MOVE_TIME
        self.direction = 1
        self.right_moves = 30
        self.left_moves = 30
        self.move_number = 15
        self.timer = self.move_time
        self._alive_columns = list(range(columns))
        self._left_alive_column = 0
        self._right_alive_column = columns - 1
        self._left_killed_columns = 0
        self._right_killed_columns = 0
        self.speed_listener = None

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.move_time
            if self.direction == 1:
                max_move = self.right_moves + self.rightAddMove
            else:
                max_move = self.left_moves + self.left_add_move

            if self.move_number >= max_move:
                if self.direction == 1:
                    self.left_moves = 30 + self.rightAddMove
                elif self.direction == -1:
                    self.right_moves = 30 + self.left_add_move
                self.direction *= -1
                self.move_number = 0
                for enemy in self:
                    enemy.rect.y += 35
                    enemy.toggle_image()
            else:
                velocity = 10 if self.direction == 1 else -10
                for enemy in self:
                    enemy.rect.x += velocity
                    enemy.toggle_image()
                self.move_number += 1

    def add_internal(self, *sprites: [Enemy]):
        super(EnemiesGroup, self).add_internal(*sprites)
        for s in sprites:
            self.enemies[s.row][s.column] = s

    def remove_internal(self, *sprites: [Enemy]):
        super(EnemiesGroup, self).remove_internal(*sprites)
        self.update_speed()

    def is_column_dead(self, column):
        for row in range(self.rows):
            if self.enemies[row][column]:
                return False
        return True

    def random_bottom(self) -> Optional[Enemy]:
        random_index = randint(0, len(self._alive_columns) - 1)
        col = self._alive_columns[random_index]
        for row in range(self.rows, 0, -1):
            enemy = self.enemies[row - 1][col]
            if enemy:
                return enemy
        return None

    def update_speed(self):
        if len(self) == 1:
            self.move_time = 200
            if self.speed_listener:
                self.speed_listener(self.move_time)
        elif len(self) <= 10:
            self.move_time = 400
            if self.speed_listener:
                self.speed_listener(self.move_time)

    def set_speed_listener(self, speed_listener: Callable):
        self.speed_listener = speed_listener

    def kill(self, enemy: Enemy):
        # on double hit calls twice for same enemy, so check before
        if not self.enemies[enemy.row][enemy.column]:
            return  # nothing to kill

        self.enemies[enemy.row][enemy.column] = None
        _is_column_dead = self.is_column_dead(enemy.column)
        if _is_column_dead:
            self._alive_columns.remove(enemy.column)

        if enemy.column == self._right_alive_column:
            while self._right_alive_column > 0 and _is_column_dead:
                self._right_alive_column -= 1
                self._right_killed_columns += 1
                self.rightAddMove = self._right_killed_columns * 5
                _is_column_dead = self.is_column_dead(self._right_alive_column)

        elif enemy.column == self._left_alive_column:
            while self._left_alive_column < self.columns and _is_column_dead:
                self._left_alive_column += 1
                self._left_killed_columns += 1
                self.left_add_move = self._left_killed_columns * 5
                _is_column_dead = self.is_column_dead(self._left_alive_column)
        enemy.kill()


def build_enemies_group(enemy_position, columns, rows):
    enemies = EnemiesGroup(columns, rows)
    for row in range(rows):
        for column in range(columns):
            enemy = build_enemy(row, column)
            enemy.rect.x = 157 + (column * 50)
            enemy.rect.y = enemy_position + (row * 45)
            enemies.add(enemy)
    return enemies
