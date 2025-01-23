import pygame as pg
from pygame.examples.cursors import image
from message import Message
from settings import *
from utils import res, SpriteSheet
import math
from environment import Explosion
from animation import Animation


class BaseNPC(pg.sprite.Sprite):

    def __init__(self, game, pos, *groups):
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites, *groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.last_update = 0
        self.frame = 0
        self.velocity = pg.Vector2(0, 0)
        self.mode = AI_IDLE
        self.hp = math.inf
        self.message = Message(self.game, self.rect.midtop, "")

    def get_damage(self, damage):
        self.mode = AI_HURT
        self.hp -= damage

    def say(self, text: str):
        if self.message.text == "":
            self.message.set_text(text)
        self.message.print()
        self.message.rect.midbottom = self.rect.midtop


class FrogSoldier(BaseNPC):
    speed = 5

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self._load_animations()
        self.animation_cycle = self.walk_right
        self.image = self.animation_cycle.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.mode = AI_PATROL

    def update(self):
        """Update control"""
        self._move()
        self._animate()

    def _move(self):
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()
        if self.mode == AI_FOLLOW_PLAYER:
            if self.game.player.rect.centerx > self.rect.x:
                self.velocity.x = 1
            elif self.game.player.rect.centerx < self.rect.x:
                self.velocity.x = -1

            if self.game.player.rect.centery > self.rect.y:
                self.velocity.y = 1
            elif self.game.player.rect.centery < self.rect.y:
                self.velocity.y = -1
        elif self.mode == AI_PATROL:
            if self.velocity.x == 0:
                self.velocity.x = 1
            if self._will_collide():
                self.velocity.x *= -1

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

    def _load_animations(self):
        sheet = SpriteSheet(res / "sprite" / "frog_soldier.png")
        w, h = sheet.w // 6, sheet.h // 5
        self.walk_right = Animation(res / "sprite" / "frog_soldier.png", 6, 5, 0, 1, 3, 100)
        self.walk_left = self.walk_right.flip()
        self.walk_up = Animation(res / "sprite" / "frog_soldier.png", 6, 5, 0, 0, 2, 100)
        self.walk_down = self.walk_up.flip()

    def _animate(self):
        if self.velocity.y > 0:
            self.animation_cycle = self.walk_down
        elif self.velocity.y < 0:
            self.animation_cycle = self.walk_up
        elif self.velocity.x > 0:
            self.animation_cycle = self.walk_right
        elif self.velocity.x < 0:
            self.animation_cycle = self.walk_left

        self.image = self.animation_cycle.get_current_frame()


class Onion(BaseNPC):
    speed = 5

    def __init__(self, game, pos):
        super().__init__(game, pos)

        self._load_animations()
        self.walk_len = [100, 100]
        self.animation_cycle = self.walk_right
        self.image = self.animation_cycle.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.mode = AI_FOLLOW_PLAYER

    def update(self):
        """Update control"""

        self._move()
        self._animate()

    def _move(self):
        if self.mode == AI_FOLLOW_PLAYER:
            self.velocity = pg.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                                       self.game.player.rect.centery - self.rect.centery)

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()

        self.velocity *= math.ceil(self.speed * self.game.dt)

        if not self._will_collide():
            self.rect.center += self.velocity
            self.phys_body.center += self.velocity
        else:
            self.velocity.x = 0
            self.velocity.y = 0

    def _will_collide(self):
        target_rect = self.phys_body.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        if target_rect.colliderect(self.game.player.rect):
            return True
        return False

    def _load_animations(self):
        sheet = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "1 - Onion Lad" / "Run_&_Jump (16 x 16).png", scale=2)
        sheet2 = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "1 - Onion Lad" / "Idle (16 x 16).png", scale=2)
        w, h = sheet.w // 2, sheet.h // 1
        self.walk_right = Animation(res / "sprite" / "Sprite Pack 2" / "1 - Onion Lad" / "Run_&_Jump (16 x 16).png", 2,
                                    1, 0, 0, 2, 90, scale=2)
        self.walk_left = self.walk_right.flip()
        self.idle = Animation(res / "sprite" / "Sprite Pack 2" / "1 - Onion Lad" / "Idle (16 x 16).png", 2, 1, 0, 0, 2,
                              [600, 100], scale=2)

    def _animate(self):

        if self.velocity.x > 0:
            self.animation_cycle = self.walk_right

        elif self.velocity.x < 0:
            self.animation_cycle = self.walk_left

        elif self.velocity.x == 0:
            self.animation_cycle = self.idle

        self.image = self.animation_cycle.get_current_frame()


class PumpkinEnemy(BaseNPC):
    speed = 100

    def __init__(self, game, pos):
        super().__init__(game, pos, game.enemies)

        self._load_animations()
        self.animation_cycle = self.walk_right
        self.image = self.animation_cycle.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.mode = AI_IDLE
        self.hp = 2
        self.hurt_update = 0

    def update(self):
        """Update control"""
        self._move()
        self._animate()

    def _load_animations(self):
        sheet = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Walking (16 x 16).png", scale=2)
        sheet2 = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Standing (16 x 16).png", scale=2)
        sheet3 = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Hurt (16 x 16).png", scale=2)
        w, h = sheet.w // 2, sheet.h // 1

        self.walk_left = Animation(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Walking (16 x 16).png", 2,
                                   1, 0, 0, 2, 90, scale=2)
        self.walk_right = self.walk_left.flip()
        self.idle = Animation(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Standing (16 x 16).png", 1, 1, 0,
                              0, 1,
                              [800, 100], scale=2)
        self.hurt = Animation(res / "sprite" / "Sprite Pack 2" / "4 - Robo Pumpkin" / "Hurt (16 x 16).png", 1, 1, 0, 0,
                              1,
                              700, scale=2)

    def _animate(self):

        if self.mode == AI_HURT:
            self.animation_cycle = self.hurt

        elif self.velocity.x > 0:
            self.animation_cycle = self.walk_right

        elif self.velocity.x < 0:
            self.animation_cycle = self.walk_left

        elif self.velocity.x == 0:
            self.animation_cycle = self.idle

        self.image = self.animation_cycle.get_current_frame()

    def _move(self):

        distance = pg.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                              self.game.player.rect.centery - self.rect.centery)
        if not self.hurt_update + self.hurt.frame_len[0] > pg.time.get_ticks():
            if int(distance.length()) < TILE_SIZE:
                if self.hp > 0:
                    self.game.player.getting_dmg(1)
                    self.mode = AI_HURT
                else:
                    self.game.player.getting_dmg(1)
                    Explosion(self.game, self.rect.center)
                    self.kill()

            elif int(distance.length()) < 4 * TILE_SIZE:
                self.mode = AI_FOLLOW_PLAYER
            else:
                self.mode = AI_IDLE

            if self.mode == AI_FOLLOW_PLAYER:
                if distance.length() > 0:
                    self.velocity = distance.normalize()
            elif self.mode == AI_HURT:
                self.hp -= 1
                self.animation_cycle = self.hurt
                self.velocity = -distance.normalize()
                self.hurt_update = pg.time.get_ticks()


            else:
                self.velocity.update()
        elif self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()

        self.rect.center += self.velocity
        self.velocity *= math.ceil(self.speed * self.game.dt)

    def _will_collide(self):
        target_rect = self.phys_body.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        if target_rect.colliderect(self.game.player.rect):
            return True
        return False


class Crab(BaseNPC):
    speed = 100

    def __init__(self, game, pos):
        super().__init__(game, pos, game.enemies)

        self._load_animations()
        self.image = self.animation_cycle.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.frame_len = [200]
        self.animation_cycle = self.walk_animation
        self.mode = AI_IDLE
        self.hp = 6
        self.hurt_update = 0

    def update(self):
        """Update control"""
        if self.hp > 0:
            self._move()
            self._animate()
        else:
            self.image = self.animation_cycle.get_current_frame()

    def _load_animations(self):
        sheet = SpriteSheet(
            res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Movement_(Flip_image_back_and_forth) (32 x 32).png",
            scale=2)
        sheet3 = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Hurt (32 x 32).png", scale=2)
        w, h = sheet.w, sheet.h
        self.walk_animation = Animation(
            res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Movement_(Flip_image_back_and_forth (32 x 32).png",
            2,
            1, 0, 0, 2, 90, scale=2)
        self.walk_animation.flip()
        self.hurt = Animation(res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Hurt (32 x 32).png", 1, 1, 0,
                              0, 1,
                              700, scale=2)

    def _animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_len[0]:
            self.last_update = now
            if self.mode == AI_HURT:
                self.animation_cycle = self.hurt
                self.frame_len = self.hurt
            elif self.velocity.length() > 0:
                self.animation_cycle = self.walk_animation
                self.image = self.animation_cycle.get_current_frame()

    def _move(self):

        distance = pg.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                              self.game.player.rect.centery - self.rect.centery)
        if not self.hurt_update + self.animation_cycle.get_current_frame() > pg.time.get_ticks():

            if self.mode == AI_FOLLOW_PLAYER:
                if distance.length() > 0:
                    self.velocity = distance.normalize()
            elif self.mode == AI_HURT:
                self.image = self.animation_cycle.get_current_frame()
                self.velocity.update()
                self.hurt_update = pg.time.get_ticks()


            else:
                self.velocity.update()
            if int(distance.length()) < 4 * TILE_SIZE:
                self.mode = AI_FOLLOW_PLAYER
            else:
                self.mode = AI_IDLE
        elif self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()

        self.rect.center += self.velocity
        self.velocity *= math.ceil(self.speed * self.game.dt)

    def _will_collide(self):
        target_rect = self.phys_body.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        if target_rect.colliderect(self.game.player.rect):
            return True
        return False
