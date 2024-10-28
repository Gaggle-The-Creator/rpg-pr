import os
import random

import pygame as pg
from utils import SpriteSheet
from utils import res
from settings import *
import math


class Player(pg.sprite.Sprite):
    speed = 180
    def __init__(self, game, sprite_sheet_path, pos):
        """Variable control"""
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites)
        sprite_sheet = SpriteSheet(sprite_sheet_path, scale=1.5)

        self.walk_len = [100, 100, 100]
        self.idle_len = [400, 400]
        self.animation_len = self.walk_len
        self._load_images(sprite_sheet)
        self._load_sounds()
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5
        self.last_update = 0
        self.frame = 0
        self.animation_cycle = self.walk_right
        self.velocity = pg.Vector2(0, 0)
        self.is_player = True

    def update(self):
        """Update control"""
        self._move()
        self._animate(250)

    def _move(self):
        """Move control"""
        self.velocity.update(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.velocity.y = -1
        if keys[pg.K_s]:
            self.velocity.y = 1
        if keys[pg.K_a]:
            self.velocity.x = -1
        if keys[pg.K_d]:
            self.velocity.x = 1

        self.velocity *= math.ceil(self.speed * self.game.dt)

        if not self._will_collide():
            self.rect.center += self.velocity
            self.phys_body.center += self.velocity
            
    def _will_collide(self):
        target_rect = self.phys_body.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        return False
    def _load_sounds(self):
        self.walking_sound = [pg.mixer.Sound(res / "sounds"/"Nature Sounds Pack"/"Footstep"/ file) for file in os.listdir(res / "sounds"/"Nature Sounds Pack"/"Footstep")]
    def _load_images(self, sheet):
        w, h = sheet.w // 5, sheet.h // 8
        self.walk_right = [sheet.get_image(i, h * 3, w, h) for i in range(0, w * 3, w)]
        self.walk_left = [pg.transform.flip(i, True, False) for i in self.walk_right]
        self.walk_up = [sheet.get_image(i, h * 2, w, h) for i in range(0, w * 3, w)]
        self.walk_down = [sheet.get_image(i, h * 1, w, h) for i in range(0, w * 3, w)]
        self.idle = [sheet.get_image(i, 0, w, h) for i in range(0, w * 2, w)]

    def _animate(self, frame_len=100):
        now = pg.time.get_ticks()
        if now - self.last_update > self.animation_len[self.frame]:
            random.choice(self.walking_sound).play()
            self.last_update = now
            if self.velocity.y > 0:
                self.animation_cycle = self.walk_down
                self.animation_len = self.walk_len
            elif self.velocity.y < 0:
                self.animation_cycle = self.walk_up
                self.animation_len = self.walk_len
            elif self.velocity.x > 0:
                self.animation_cycle = self.walk_right
                self.animation_len = self.walk_len
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_left
                self.animation_len = self.walk_len
            elif  self.velocity.length() == 0:
                self.animation_cycle = self.idle
                self.animation_len = self.idle_len


            self.frame = (self.frame + 1) % len(self.animation_cycle)

            self.image = self.animation_cycle[self.frame]


