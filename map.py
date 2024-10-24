
import json
import pygame as pg
from settings import *
import pytmx
from utils import res
import NPC



class TileMap:


    def __init__(self, game, image_path,  map_: str, next_map: str):


        # self.width = len(data_list[0]) * TILE_SIZE
        # self.height = len(data_list) * TILE_SIZE
        self.game = game
        self.tmx_map = pytmx.load_pygame(res / "map" / map_)
        self.width = self.tmx_map.tilewidth * self.tmx_map.width
        self.height = self.tmx_map.tileheight * self.tmx_map.height


        self._tiles = pg.sprite.Group()
        self._load_tiles(game)
        self.next_map = next_map
        # self._load_npc()





    def _load_tiles(self, game):
        i = 0
        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    if layer.name == "player":
                        self.game.player.rect.center = x * TILE_SIZE, y * TILE_SIZE
                        self.game.player.phys_body.center = x * TILE_SIZE, y * TILE_SIZE
                    elif layer.name == "onion":
                        NPC.Onion(self.game, (x * TILE_SIZE, y * TILE_SIZE))
                    elif layer.name == "frog":
                        NPC.FrogSoldier(self.game, (x * TILE_SIZE, y * TILE_SIZE))


                    else:
                        self._tiles.add(Tile(game, x,y,tile, layer=i))

            i += 1

    def _load_npc(self):
        with open(res/"map"/"map_enemies.json", "r") as f:
            data = json.load(f)

        for enemy in data["npc"]:
            if enemy["name"] == "Onion":
                NPC.Onion(self.game, enemy["pos"])
            if enemy["name"] == "FrogSoldier":
                NPC.FrogSoldier(self.game, enemy["pos"])

    def _unload_tiles(self):
        for sprite in self.game.all_sprites:
            if not hasattr(sprite, "is_player"):
                sprite.kill()


    def change_level(self):
        self._unload_tiles()
        # self.game.player.rect.center = 100, 100
        # self.game.player.phys_body.center = 100, 100

        self.tmx_map = pytmx.load_pygame(res / "map" / self.next_map)
        self.width = self.tmx_map.tilewidth * self.tmx_map.width
        self.height = self.tmx_map.tileheight * self.tmx_map.height
        self._load_tiles(self.game)




class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, image, layer=GROUND_LAYER):
        self._layer = layer
        if layer == 2:
            super().__init__(game.all_sprites, game.walls)
        else:
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

    def apply(self, entity_rect: pg.Rect):
        return entity_rect.move(self.offset)

    def update(self, target):
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2

        x = min(x, 0)
        y = min(y, 0)
        x = max(x, -self.map_width + SCREEN_WIDTH)
        y = max(y, -self.map_height + SCREEN_HEIGHT)

        self.offset = (x, y)
