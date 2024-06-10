import pygame as pg
import sys
from pathlib import Path


res = Path(sys.argv[0]).parent / "res"


class SpriteSheet:
    """Class for control over sprite sheetss"""
    def __init__(self, fp, scale=1):
        """Loading image form path"""
        self.sheet = pg.image.load(fp).convert_alpha()
        self.sheet = pg.transform.scale_by(self.sheet, scale)
        self.w, self.h = self.sheet.get_size()

    def get_image(self, x, y, width, height):
        """Returns part of a sprite sheet"""
        return self.sheet.subsurface(x, y, width, height)