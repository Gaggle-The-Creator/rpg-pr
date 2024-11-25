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


        self.arc_size = 0.1
        self.image = self.attack_image
        self.rect = self.attack_image.get_rect()



    def attack(self, user_rect, mouse_pos):
        self.attack_image = pg.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pg.SRCALPHA)
        if  pg.time.get_ticks() - self.last_attack < self.attack_speed:
            angle = Vector2.angle_to(Vector2( mouse_pos[0] - user_rect.centerx , mouse_pos[1] - user_rect.centery ), (1, 0))

            self.rect.center = user_rect.center

            pg.draw.arc(self.attack_image, pg.Color("black"), (0,0,TILE_SIZE * 3 , TILE_SIZE * 3 ),
                        math.radians(angle) - self.arc_size, math.radians(angle ) + self.arc_size, width=16 // 2)

            self.image = self.attack_image
            self.arc_size += 0.1
        else:
            self.last_attack = pg.time.get_ticks()
            self.arc_size= 0.1
        for enemy in self.game.enemies:
            if enemy.rect.colliderect(self.rect):
                print(enemy)
                enemy.mode = AI_HURT

        #attack sounds
        random.choice(self.punches_sound).play()
