import numpy as np
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

        dx, dy, dz = 0, 0, 0
        speed = 0.05

        if self.direction[0] != 0:
            dx = np.cos(world.camera.yaw) * self.direction[0] * speed
            dy = np.sin(world.camera.yaw) * -self.direction[0] * speed
        elif self.direction[1] != 0:
            dx = np.cos(world.camera.yaw - np.pi/2) * -self.direction[1] * speed
            dy = np.sin(world.camera.yaw - np.pi/2) * self.direction[1] * speed
        elif self.direction[2] != 0:
            dz = self.direction[2] * -speed

        world.camera.pos = (
            x + dx,
            y + dy,
            z + dz,
        )


class TurnYawCameraAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_world(self, world, render):
        world.camera.yaw += 0.05 * self.direction
        if world.camera.yaw > np.pi:
             world.camera.yaw = -np.pi
        elif world.camera.yaw < -np.pi:
             world.camera.yaw = np.pi


class TurnPitchCameraAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_world(self, world, render):
        world.camera.pitch += 0.05 * self.direction
        if world.camera.pitch > np.pi/2:
             world.camera.pitch = np.pi/2
        elif world.camera.pitch < -np.pi/2:
             world.camera.pitch = -np.pi/2

