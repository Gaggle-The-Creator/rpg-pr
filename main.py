import pygame as pg

from utils import res
from settings import *
from player import Player
from map import TileMap
from map import Camera

class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        pg.display.set_icon(pg.image.load(res / "sprite" / "frog.png"))
        self.running = True


    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = Player(game,res / "sprite" / "player_sheet.png", (100, 100))
        self.map = TileMap(self, res / "map"/ "21489107669003fddf5293.96874412map (1).csv", res / "map"/ "2148910766900407bcfce9.26900631rpg_tileset (1).png", 16)
        self.camera = Camera(self.map.width, self.map.height)
    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def _draw(self):
        self.screen.fill((255, 255, 255))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
