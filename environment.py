import pygame as pg

from message import Message
from settings import *
from utils import res, SpriteSheet

import math

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self._load_animations()
        self.image = self.explosion[0]
        self.rect = self.image.get_rect(center=pos)
        self.frame = 0
        self.frame_len = 200
        self.last_update = 0



    def _load_animations(self):

        sheet = SpriteSheet(res / "environment" / "explosion.png", scale=2)
        w, h = sheet.w // 6, sheet.h // 1
        self.explosion = [sheet.get_image(i, 0, w, h) for i in range(0, w * 6, w)]

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_len:
            self.last_update = now
            self.frame += 1
            self.image = self.explosion[self.frame]
            if self.frame == 5:
               self.kill()

