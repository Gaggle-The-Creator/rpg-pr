import os

import pygame as pg

from utils import res
from settings import *
from player import Player
from map import TileMap
from map import Camera
from NPC import NPC
from NPC import FrogSoldier
from NPC import Onion
from NPC import PumpkinEnemy


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
    def new(self):

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.player = Player(game, res / "sprite" / "Panda.png", (100, 100))
        self.map = TileMap(self,res / "map"/ "tile_set.png", map_="frog_map.tmx", next_map="desert_map.tmx")
        self.enemies = pg.sprite.Group()
        PumpkinEnemy(self, (400, 400))


        pg.mixer.music.load(res / "music" / self.music_tracks[1])
        pg.mixer.music.play()
        self.camera = Camera(self.map.width, self.map.height)


    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # self.fps()

        if self.player.rect.y > self.map.height:
            self.player.center = (100, 100)
            self.map.change_level()

        pg.sprite.spritecollide(self.player, self.enemies, True)

    def _draw(self):
        self.screen.fill((255, 255, 255))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        # self._draw_player_hitbox()
        pg.display.flip()

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
