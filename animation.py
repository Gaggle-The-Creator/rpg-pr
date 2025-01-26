from copy import copy

import pygame as pg

from message import Message
from settings import *
from utils import res, SpriteSheet
import math
from environment import Explosion

class Animation:
    def __init__(self, fp, width, height, x, y, frames, frame_len=None, scale=1):
        self.time = []
        self.frames = []
        sheet= SpriteSheet(fp,scale)
        w, h = sheet.w // width, sheet.h // height
        self.frames = [sheet.get_image(i, h * y, w, h) for i in range(x * w, w * frames, w)]
        if frame_len is None:
            self.frame_len = [200] * len(self.frames)
        elif isinstance(frame_len, int):
            self.frame_len = [frame_len] * frames
        else:
            self.frame_len = frame_len
        self.last_update = pg.time.get_ticks()
        self.animation_len = frames
        self.frame = 0


    def flip(self):
        # frames = [pg.transform.flip(i, True, False) for i in flipped.frames]
        # flipped = Animation()
        flipped = copy(self)
        flipped.frames = [pg.transform.flip(i, True, False) for i in flipped.frames]
        return flipped
    def get_current_frame(self):
        if pg.time.get_ticks() - self.last_update > self.frame_len[self.frame]:
            self.frame = (self.frame + 1) % self.animation_len
            self.last_update = pg.time.get_ticks()

        return self.frames[self.frame]

    def add_frame(self, frame, time):
        self.frames.append(frame)
        self.animation_len += 1
        self.frame_len.append(time)

