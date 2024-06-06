import pygame as pg
import sys
from pathlib import Path


res = Path(sys.argv[0]).parent / "res"


class SpriteSheet:
    """Class for control over sprite sheets"""
    def __init__(self, fp):
        """Loading image form path"""
        self.sheet = pg.image.load(fp).convert_alpha()

    def get_image(self, x, y, width, height):
        """Returns part of a sprite sheet"""
        return self.sheet.subsurface(x, y, width, height)