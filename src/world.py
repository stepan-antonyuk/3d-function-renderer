from mesh import Plane
from camera import Camera


class World:
    def __init__(self):
        self.mode = "map"
        self.gravity = -5
        self.camera = Camera((13.0, 0.5, 2))
        self.objects = [Plane((0.0, 0.0, 0.0))]


    def update(self):  # does something every frame, could be useful for enemy AI or update some values
        if self.mode == "game":
            pass
        pass

    def setup(self, coords_converter):
        if self.mode == "game":
            pass
        pass
