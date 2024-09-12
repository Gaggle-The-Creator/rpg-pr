import pygame as pg
from settings import *


class NPC(pg.sprite.Sprite):

    def __init__(self, game, pos, image):
        self._layer = GROUND_LAYER
        self.game = game
        super().__init__(game.all_sprites, game.walls)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.velocity = pg.Vector2(0,0)
        self.speed = 7
        self.mode = "FOLLOW PLAYER"

    def update(self):
        if self.mode == "FOLLOW PLAYER":
            if self.game.player.rect.centerx > self.rect.x:
                self.velocity[0] = 1
            elif self.game.player.rect.centerx < self.rect.x:
                self.velocity[0] = -1

            if self.game.player.rect.centery > self.rect.y:
                self.velocity[1] = 1
            elif self.game.player.rect.centery < self.rect.y:
                self.velocity[1] = -1

            target_rect = self.rect.move(self.velocity * self.speed)

            if not target_rect.colliderect(self.game.player.rect):
                self.rect.center += self.speed * self.velocity

