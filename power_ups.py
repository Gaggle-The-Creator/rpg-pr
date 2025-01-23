import math
import os
import random

import pygame as pg
from pygame import Vector2
from pygame.sprite import collide_rect

from settings import *
from utils import res, SpriteSheet

class PowerupHealth(pg.sprite.Sprite):

    def __init__(self,game, x, y):
        self._layer = PLAYER_LAYER
        super().__init__(game.all_sprites, game.power_ups)
        self.spritesheet = SpriteSheet(res/"sprite"/"roguelikeitems.png")
        self.image = self.spritesheet.get_image(12 * 16, 4 * 16, 16, 16)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def use(self):
        if self.game.player.hp < 10:
            self.game.player.hp += 1





