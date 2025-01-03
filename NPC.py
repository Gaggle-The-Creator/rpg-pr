import pygame as pg

from message import Message
from settings import *
from utils import res, SpriteSheet
import math
from environment import Explosion


class NPC(pg.sprite.Sprite):

    def __init__(self, game, pos, image):
        self._layer = GROUND_LAYER
        self.game = game
        super().__init__(game.all_sprites, game.walls)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.velocity = pg.Vector2(0, 0)
        self.speed = 7
        self.mode = "FOLLOW PLAYER"
        self.message = Message(game, (pos[0] - 80, pos[1] - 60), "Hey, frog!")

    def update(self):
        if 2000 < pg.time.get_ticks() < 2020:
            self.message.set_text("this game is P2W")
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
            else:
                self.mode = "SPEAK"

        elif self.mode == "SPEAK":
            if self.rect.colliderect(self.game.player):
                self.message.rect.center = self.rect.centerx - 80, self.rect.centery - 60
                self.message.print()
            elif self.message.groups():
                self.message.reset()


class FrogSoldier(pg.sprite.Sprite):
    speed = 5

    def __init__(self, game, pos):
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites)
        self._load_animations()
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.last_update = 0
        self.frame = 0
        self.animation_cycle = self.walk_right
        self.velocity = pg.Vector2(0, 0)
        self.mode = AI_PATROL

    def update(self):
        """Update control"""
        self._move()
        self._animate(100)

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
        self.walk_right = [sheet.get_image(i, h, w, h) for i in range(0, w * 3, w)]
        self.walk_left = [pg.transform.flip(i, True, False) for i in self.walk_right]
        self.walk_up = [sheet.get_image(i, 0, w, h) for i in range(2, w * 4, w)]
        self.walk_down = [sheet.get_image(i, 0, w, h) for i in range(0, w * 2, w)]

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

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            # print(self.frame)
            self.image = self.animation_cycle[self.frame]


class Onion(pg.sprite.Sprite):
    speed = 5

    def __init__(self, game, pos):
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites)
        self._load_animations()
        self.walk_len = [100, 100]
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.last_update = 0
        self.frame = 0
        self.frame_len = [200]
        self.animation_cycle = self.walk_right
        self.velocity = pg.Vector2(0, 0)
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
        self.walk_right = [sheet.get_image(i, 0, w, h) for i in range(0, w * 2, w)]
        self.walk_left = [pg.transform.flip(i, True, False) for i in self.walk_right]
        self.idle = [sheet2.get_image(i, 0, w, h) for i in range(0, w * 2, w)]
        self.idle_len = [600, 100]

    def _animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_len[self.frame]:
            self.last_update = now

            if self.velocity.x > 0:
                self.animation_cycle = self.walk_right
                self.frame_len = self.walk_len
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_left
                self.frame_len = self.walk_len
            elif self.velocity.x == 0:
                self.animation_cycle = self.idle
                self.frame_len = self.idle_len

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            # print(self.frame)
            self.image = self.animation_cycle[self.frame]


class PumpkinEnemy(pg.sprite.Sprite):
    speed = 100
    def __init__(self, game, pos):
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites, game.enemies)
        self._load_animations()
        self.walk_len = [100, 100]
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.last_update = 0
        self.frame = 0
        self.frame_len = [200]
        self.animation_cycle = self.walk_right
        self.velocity = pg.Vector2(0, 0)
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
        self.walk_left = [sheet.get_image(i, 0, w, h) for i in range(0, w * 2, w)]
        self.walk_right = [pg.transform.flip(i, True, False) for i in self.walk_left]
        self.idle = [sheet2.get_image(0, 0, w, h)]
        self.idle_len = [800, 100]
        self.hurt = [sheet3.get_image(0, 0, w, h)]
        self.hurt_len = [700]

    def _animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_len[self.frame]:
            self.last_update = now
            if self.mode == AI_HURT:
                self.animation_cycle = self.hurt
                self.frame_len = self.hurt_len
            elif self.velocity.x > 0 :
                self.animation_cycle = self.walk_right
                self.frame_len = self.walk_len
            elif self.velocity.x < 0 :
                self.animation_cycle = self.walk_left
                self.frame_len = self.walk_len
            elif self.velocity.x == 0:
                self.animation_cycle = self.idle
                self.frame_len = self.idle_len

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            self.image = self.animation_cycle[self.frame]


    def _move(self):

        distance = pg.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                              self.game.player.rect.centery - self.rect.centery)
        if not self.hurt_update + self.hurt_len[0] > pg.time.get_ticks():
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
                self.image = self.hurt[0]
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

class Crab(pg.sprite.Sprite):
    speed = 100

    def __init__(self, game, pos):
        self._layer = PLAYER_LAYER
        self.game = game
        super().__init__(game.all_sprites, game.enemies)
        self._load_animations()
        self.walk_len = [100, 100]
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.phys_body = pg.Rect(self.rect.x, self.rect.y,
                                 self.rect.w * 0.5, self.rect.h * 0.25)
        self.phys_body.centerx = self.rect.centerx
        self.phys_body.bottom = self.rect.bottom - 5

        self.last_update = 0
        self.frame = 0
        self.frame_len = [200]
        self.animation_cycle = self.walk_animation
        self.velocity = pg.Vector2(0, 0)
        self.mode = AI_IDLE
        self.hp = 6
        self.hurt_update = 0

    def update(self):
        """Update control"""
        if self.hp > 0:
            self._move()
            self._animate()

    def _load_animations(self):
        sheet = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Movement_(Flip_image_back_and_forth) (32 x 32).png", scale=2)
        sheet3 = SpriteSheet(res / "sprite" / "Sprite Pack 2" / "9 - Snip Snap Crab" / "Hurt (32 x 32).png", scale=2)
        w, h = sheet.w, sheet.h
        self.walk_animation = [sheet.get_image(0,0, w, h)]
        self.walk_animation.append(pg.transform.flip(self.walk_animation[0], True, False))
        self.hurt = [sheet3.get_image(0, 0, w, h)]
        self.hurt_len = [200]

    def _animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_len[0]:
            self.last_update = now
            if self.mode == AI_HURT:
                self.animation_cycle = self.hurt
                self.frame_len = self.hurt_len
            elif self.velocity.length() > 0:
                self.animation_cycle = self.walk_animation

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            self.image = self.animation_cycle[self.frame]

    def _move(self):

        distance = pg.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                              self.game.player.rect.centery - self.rect.centery)
        if not self.hurt_update + self.hurt_len[0] > pg.time.get_ticks():




            if self.mode == AI_FOLLOW_PLAYER:
                if distance.length() > 0:
                    self.velocity = distance.normalize()
            elif self.mode == AI_HURT:
                self.hp -= 1
                self.image = self.hurt[0]
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


