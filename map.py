import csv
import pygame as pg
from settings import *


class TileMap:
    def __init__(self, game, csv_path, image_path, img_tile_size):
        data_list = self._csv_to_list(csv_path)
        image_list = self._parse_image(image_path, img_tile_size)
        self._load_tiles(game, data_list, image_list)
        self.width = len(data_list[0]) * TILE_SIZE
        self.height = len(data_list) * TILE_SIZE
    @staticmethod
    def _csv_to_list(fp):
        with open(fp) as f:
            reader = csv.reader(f)
            data = list(reader)

        return data

    @staticmethod
    def _parse_image(fp, img_tile_size):
        image = pg.image.load(fp).convert()
        image_list = []

        if TILE_SIZE != img_tile_size:
            scale = TILE_SIZE // img_tile_size
            image = pg.transform.scale_by(image, scale)

        width, height = image.get_size()
        for y in range(0, height, TILE_SIZE):
            for x in range(0, width, TILE_SIZE):
                tile = image.subsurface(x, y, TILE_SIZE, TILE_SIZE)
                image_list.append(tile)
        return image_list

    @staticmethod
    def _load_tiles(game, data, images):
        for y, row in enumerate(data):
            for x, index in enumerate(row):
                Tile(game, x, y, images[int(index)])


class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self._layer = GROUND_LAYER
        super().__init__(game.all_sprites)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = TILE_SIZE * x
        self.rect.y = TILE_SIZE * y


"""allows us to follow the player"""


class Camera:
    def __init__(self, map_width, map_height):
        self.offset = (0, 0)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.offset)

    def update(self, target):
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2

        x = min(x, 0)
        y = min(y, 0)
        x = max(x, -self.map_width + SCREEN_WIDTH)
        y = max(y, -self.map_height + SCREEN_HEIGHT)

        self.offset = (x, y)
