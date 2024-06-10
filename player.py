import pygame as pg
from utils import SpriteSheet


class Player(pg.sprite.Sprite):
    speed = 8

    def __init__(self, sprite_sheet_path, pos):
        """Variable control"""
        super().__init__()
        sprite_sheet = SpriteSheet(sprite_sheet_path)
        self._load_images(sprite_sheet)
        self.image = self.walk_right[0]
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

    def _load_images(self, sheet):
        w, h = sheet.w // 4, sheet.h // 4
        self.walk_right = [sheet.get_image(i, h * 2, 32, 32) for i in range(0, w * 4, w)]
        self.walk_left = [sheet.get_image(i, h, 32, 32) for i in range(0, w * 4, w)]
        self.walk_up = [sheet.get_image(i, h * 3,  32, 32) for i in range(0, w * 4, w)]
        self.walk_down = [sheet.get_image(i, 0, 32, 32) for i in range(0, w * 4, w)]
