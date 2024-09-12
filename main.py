import pygame as pg

from utils import res
from settings import *
from player import Player
from map import TileMap
from map import Camera
from NPC import NPC

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
        self.walls = pg.sprite.Group()
        self.player = Player(game,res / "sprite" / "player_sheet.png", (100, 100))
        self.map = TileMap(self, res / "map"/ "21489107669003fddf5293.96874412map (1).csv", res / "map"/ "2148910766900407bcfce9.26900631rpg_tileset (1).png", 16)
        self.npc = NPC(self, (100, 100), self.map.image_list[124])
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
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        # self._draw_player_hitbox()
        pg.display.flip()

    def _draw_player_hitbox(self):
        pg.draw.rect(self.screen, (255, 0, 0), self.camera.apply(self.player.rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        pg.draw.rect(self.screen, (0, 0, 255), self.camera.apply(self.player.phys_body))
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
