import pygame as pg
import pygame.freetype

from settings import TILE_SIZE
from utils import res

w, h = 272, 128

pg.init()
screen = pg.display.set_mode((w * 2, h * 2))

font = pg.freetype.Font(None, 16)
image = pg.image.load(res / "map" / "tile_set.png")
image = pg.transform.scale(image, (w * 2, h * 2))

i = 0

for y in range(0, h * 2, TILE_SIZE):
    for x in range(0, w * 2, TILE_SIZE):
        font.render_to(image, (x + 10, y + 10), str(i))
        i += 1

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.blit(image, (0, 0))
    pg.display.flip()
