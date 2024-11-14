import numpy as np
from objLoader import read_obj


class GenericObject():
    def __init__ (self, pos, points, triangles):
        self.pos = pos
        self.points = points
        self.triangles = triangles

class Plane(GenericObject):
    def __init__ (self, pos):
        points = np.asarray([
            [1.0, 0.0, 1.0, 1],
            [-1.0, 0.0, 1.0, 1],
            [1.0, 0.0, -1.0, 1],
            [-1.0, 0.0, -1.0, 1],
            [1.0, 0.0, -1.0, 1],
            [-1.0, 0.0, 1.0, 1],
        ])
        triangles = np.asarray([[0,1,2],[3,4,5]])
        super(Plane, self).__init__(pos, points, triangles)
    
class Test(GenericObject):
    def __init__ (self, pos):
        points = np.asarray([[1, 1, 1, 1], [4, 2, 0, 1], [1, .5, 3, 1]])
        triangles = np.asarray([[0,1,2]])
        points, triangles = read_obj('finfet.obj')
        super(Test, self).__init__(pos, points, triangles)

class Fun(GenericObject):
    def __init__ (self, pos):
        self.minp = [-2,-2,0]
        self.maxp = [2,2,2]
        self.stepx = 0.4
        self.stepy = 0.4

        points, triangles = self.gpt()
        super(Fun, self).__init__(pos, points, triangles)

    def black_box(self, x, y):
        return x**2 + y**2

    def gpt(self):
        points = []
        triangles = []
        point_index_map = {}  # Dictionary to map (x, y) grid coordinates to point indices

        # Generate points
        x_values = np.arange(self.minp[0], self.maxp[0] + self.stepx, self.stepx)
        y_values = np.arange(self.minp[1], self.maxp[1] + self.stepy, self.stepy)

        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                z = self.black_box(x, y)
                point = [x, y, z, 1]
                points.append(point)
                point_index_map[(i, j)] = len(points) - 1  # Store index of this point

        # Generate triangles based on grid layout
        num_x = len(x_values)
        num_y = len(y_values)

        for i in range(num_x - 1):
            for j in range(num_y - 1):
                # Each grid cell is divided into two triangles
                # Get the indices of the four corners of this cell
                p1 = point_index_map[(i, j)]
                p2 = point_index_map[(i + 1, j)]
                p3 = point_index_map[(i, j + 1)]
                p4 = point_index_map[(i + 1, j + 1)]

                # Triangle 1: (p1, p2, p4)
                triangles.append([p1, p2, p4])
                # Triangle 2: (p1, p4, p3)
                triangles.append([p1, p4, p3])

        return np.array(points), np.array(triangles)

