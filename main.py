import pygame as pg

from utils import res
from settings import *
from player import Player


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        pg.display.set_icon(pg.image.load(res / "sprite" / "frog.png"))
        self.running = True

    def new(self):
        player = Player(res / "sprite" / "player_sheet.png", (100, 100))
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(player)

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _update(self):
        self.all_sprites.update()

    def _draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()


if __name__ =="__main__":

    game = Game()
    game.new()
    game.run()
