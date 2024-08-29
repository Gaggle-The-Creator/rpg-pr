import pygame as pg
from utils import SpriteSheet
from settings import *


class Player(pg.sprite.Sprite):
    speed = 8

    def __init__(self, game, sprite_sheet_path, pos):
        """Variable control"""
        self._layer = PLAYER_LAYER
        super().__init__(game.all_sprites)
        sprite_sheet = SpriteSheet(sprite_sheet_path, scale=2)
        self.animation_len = 4
        self._load_images(sprite_sheet)
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.last_update = 0
        self.frame = 0
        self.animation_cycle = self.walk_right
        self.velocity = pg.Vector2(0, 0)

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

        self.velocity *= self.speed

        self.rect.center += self.velocity

    def _load_images(self, sheet):
        w, h = sheet.w // self.animation_len, sheet.h // self.animation_len
        self.walk_right = [sheet.get_image(i, h * 2, w, h) for i in range(0, w * 4, w)]
        self.walk_left = [sheet.get_image(i, h, w, h) for i in range(0, w * 4, w)]
        self.walk_up = [sheet.get_image(i, h * 3, w, h) for i in range(0, w * 4, w)]
        self.walk_down = [sheet.get_image(i, 0, w, h) for i in range(0, w * 4, w)]

    def _animate(self, frame_len=100):
        now = pg.time.get_ticks()
        if now - self.last_update > frame_len and self.velocity.length() > 0:
            self.last_update = now
            if self.velocity.y > 0:
                self.animation_cycle = self.walk_down
            elif self.velocity.y < 0:
                self.animation_cycle = self.walk_up
            elif self.velocity.x > 0:
                self.animation_cycle = self.walk_right
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_left

            self.frame = (self.frame + 1) % self.animation_len

            self.image = self.animation_cycle[self.frame]
