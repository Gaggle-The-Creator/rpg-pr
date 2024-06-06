import pygame as pg
from utils import SpriteSheet


class Player(pg.sprite.Sprite):
    speed = 5

    def __init__(self, sprite_sheet_path, pos):
        """Variable control"""
        super().__init__()
        self.sprite_sheet = SpriteSheet(sprite_sheet_path)
        self.image = self.sprite_sheet.get_image(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        """Update control"""
        self._move()

    def _move(self):
        """Move control"""
        self.velocity = pg.Vector2(0, 0)
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
