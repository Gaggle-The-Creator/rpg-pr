import math
import os
import random

import pygame as pg
from pygame import Vector2

from settings import *
from utils import res


class Fists(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER + 1
        super().__init__(game.all_sprites)

        self.damage = 1
        self.attack_speed = 200
        self.game = game
        self.last_attack = pg.time.get_ticks()
        self.attack_image = pg.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pg.SRCALPHA)
        self.idle_image = pg.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pg.SRCALPHA)
        self.punches_sound = [pg.mixer.Sound(res / "sounds" / "swishes" / i) for i in os.listdir(res/"sounds"/"swishes")]
        self.angle = 0
        self.attack_mode = False
        self.arc_size = 0.1
        self.image = self.attack_image
        self.rect = self.attack_image.get_rect()



    def attack(self, user_rect, mouse_pos):

        if  pg.time.get_ticks() - self.last_attack > self.attack_speed:

            #attack sounds
            random.choice(self.punches_sound).play()
            self.attack_image = pg.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pg.SRCALPHA)
            self.rect.center = user_rect.center
            self.arc_size = 0.1
            self.angle = angle = Vector2.angle_to(Vector2(mouse_pos[0] - user_rect.centerx, mouse_pos[1] - user_rect.centery),
                                     (1, 0))
            self.rect.center = user_rect.center
            self.image = self.attack_image
            self.last_attack = pg.time.get_ticks()
            self.attack_mode = True

            for enemy in self.game.enemies:
                if enemy.rect.colliderect(self.rect):
                    enemy.get_damage(1)
        if self.attack_mode:

            color = 256 - int(self.arc_size * 127), 0, 0, 256 - int(self.arc_size * 120)
            attack_width = int(self.arc_size * TILE_SIZE) // 2


            pg.draw.arc(self.attack_image,color, (0, 0, TILE_SIZE * 3, TILE_SIZE * 3),
                        math.radians(self.angle) - self.arc_size, math.radians(self.angle) + self.arc_size, width=attack_width)

            self.arc_size += 0.1
            if self.arc_size > 2:


                self.attack_mode = False
class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction, game):
        super(Ball, self).__init__(game.all_sprites)

        self.direction = pg.Vector2(direction[0] - player_rect.centerx,
                              direction[1] -player_rect.centery).normalize()
        self.speed = 10

        self.image = pg.image.load(res/"sprite"/"ball.png" )
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.rect.center = player_rect.center
        self.timer = pg.time.get_ticks()
    def update(self):
        self.rect.center += self.direction * self.speed
        if pg.time.get_ticks() - 500 > self.timer:
            self.kill()
