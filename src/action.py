from world import World
from render import Renderer


class Action:
    # pylint: disable=no-self-use
    def is_done(self):
        return False

    def change_world(self, world: World, render: Renderer):  #
        pass

    # def change_renderer(self, render: Renderer):
    #     pass


class DoneAction(Action):
    def is_done(self):
        return True


class NopAction(Action):
    pass


class DebugAction(Action):
    def __init__(self, message):
        self.message = message

    def change_world(self, world, render):
        print(self.message)


class ChangeModeAction(Action):
    def __init__(self, mode):
        self.mode = mode

    def change_world(self, world, render):
        world.mode = self.mode


class AddBlockAction(Action):
    def change_world(self, universe, render):
        pass


class MoveCameraAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_world(self, world, render):
        x, y, z = world.camera.pos
        world.camera.pos = (
            x + self.direction[0],
            y + self.direction[1],
            z + self.direction[2],
        )


class TurnYawCameraAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_world(self, world, render):
        world.camera.yaw += 0.05 * self.direction


class TurnPitchCameraAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_world(self, world, render):
        world.camera.pitch += 0.05 * self.direction

