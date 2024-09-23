import numpy as np


class Triangle():
    def __init__ (self, point1, point2, point3):
        self.points = np.asarray([point1, point2, point3])
        self.triangle = np.asarray([[0, 1, 2]])

class GenericObject():
    def __init__ (self, pos, angle=(0.0, 0.0, 1.0), triangles=[]):
        self.pos = pos
        self.shape = triangles
        self.angle = angle

class Plane(GenericObject):
    def __init__ (self, pos, angle=(0.0, 0.0, 1.0)):
        shape = [
            Triangle(
                (1.0, 1.0, 0.0, 1, 1),
                (-1.0, 1.0, 0.0, 1, 1),
                (1.0, -1.0, 0.0, 1, 1),
            ),
            Triangle(
                (-1.0, -1.0, 0.0, 1, 1),
                (1.0, -1.0, 0.0, 1, 1),
                (-1.0, 1.0, 0.0, 1, 1),
            ),
        ]
        super(Plane, self).__init__(pos, angle, shape)
    
