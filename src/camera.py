import math
import cmath
import numpy as np


class Camera():
    def __init__(self, pos):
        # free parameters
        self.pos = pos
        self.yaw = 3.3
        self.pitch = 0
        self.lookdir = (0.0, 0.0, 1.0)
        self.updir = (0.0, 1.0, 0.0)

    def update(self, world):
        pass

