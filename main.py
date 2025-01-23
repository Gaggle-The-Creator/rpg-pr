import os

import pygame as pg

from utils import res
from settings import *
from player import Player
from map import TileMap
from map import Camera
from NPC import BaseNPC
from NPC import FrogSoldier
from NPC import Onion
from NPC import PumpkinEnemy
from NPC import Crab


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        pg.display.set_icon(pg.image.load(res / "sprite" / "frog.png"))
        self.running = True
        self.dt = 0

        self.music_tracks = [file for file in os.listdir(res / "music") if file[-3:] == "wav"]
        # UI images
        self.health_bar = pg.image.load(res / "sprite" / "sp_bar_health_strip12.png")
        scale = TILE_SIZE // 16
        self.health_bar = pg.transform.scale_by(self.health_bar, scale)
        self.health_bar = [self.health_bar.subsurface((i, 0, 64 * scale, 16 * scale)) for i in range(0, 768 * scale, 64 * scale)]

    def new(self):

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        self.player = Player(game, res / "sprite" / "Panda.png", (100, 100))
        self.map = TileMap(self, res / "map" / "tile_set.png", map_="frog_map.tmx", next_map="desert_map.tmx")
        self.enemies = pg.sprite.Group()
        Crab(self, (400, 400))
        PumpkinEnemy(self,(300, 300))

        pg.mixer.music.load(res / "music" / self.music_tracks[1])
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()
        self.camera = Camera(self.map.width, self.map.height)

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.player.balls.update()
        hits = pg.sprite.groupcollide(self.enemies, self.player.balls, False, True)
        for hit in hits:
            hit.get_damage(0.007)
        heals = pg.sprite.spritecollide(self.player, self.power_ups, True)
        for heal in heals:
            heal.use()

        for npc in self.all_sprites:
            if isinstance(npc, FrogSoldier):
                npc.say("e")

        # self.fps()

        if self.player.rect.y > self.map.height:
            self.player.center = (100, 100)
            self.map.change_level()

    def _draw(self):
        self.screen.fill((255, 255, 255))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
            if hasattr(sprite, "hp"):
                pg.draw.rect(self.screen, (255, 0, 0), (sprite.rect.topleft, (sprite.hp * 8, 8)))

        self._draw_ui()
        # self._draw_player_hitbox()
        pg.display.flip()

    def _draw_ui(self):
        self.screen.blit(self.health_bar[self.player.hp], (10, 10))

    def _draw_player_hitbox(self):
        pg.draw.rect(self.screen, (255, 0, 0), self.camera.apply(self.player.rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        pg.draw.rect(self.screen, (0, 0, 255), self.camera.apply(self.player.phys_body))

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self._events()
            self._update()
            self._draw()

    def fps(self):
        print("FPS:", int(self.clock.get_fps()))


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
