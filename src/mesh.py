import numpy as np


class GenericObject():
    def __init__ (self, pos, points, triangles):
        self.pos = pos
        self.points = points
        self.triangles = triangles

class Plane(GenericObject):
    def __init__ (self, pos):
        points = np.asarray([
            [1.0, 1.0, 0.0, 1, 1],
            [-1.0, 1.0, 0.0, 1, 1],
            [1.0, -1.0, 0.0, 1, 1],
            [-1.0, -1.0, 0.0, 1, 1],
            [1.0, -1.0, 0.0, 1, 1],
            [-1.0, 1.0, 0.0, 1, 1],
        ])
        triangles = np.asarray([[0,1,2],[3,4,5]])
        super(Plane, self).__init__(pos, points, triangles)
    
class Test(GenericObject):
    def __init__ (self, pos):
        points = np.asarray([[1, 1, 1, 1, 1], [4, 2, 0, 1, 1], [1, .5, 3, 1, 1]])
        triangles = np.asarray([[0,1,2]])
        super(Test, self).__init__(pos, points, triangles)
