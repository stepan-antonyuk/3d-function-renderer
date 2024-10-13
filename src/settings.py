import pygame

from action import *


FPS = 60
HOR_SPEED = 12

TRANSLATION_MAP = {
    'game': {
        'key_pressed': {
            # add some methods that are executed when key is pressed
        },
        'key_not_pressed': {
            # add some methods that are executed when key is not pressed
        },
        'key_down': {
            # add some methods that are executed when key is down pressed
            pygame.K_e: ChangeModeAction("map"),
        },
        'key_up': {
            # add some methods that are executed when key is up pressed
        },
        'mouse_pressed': {
            # add some methods that are executed when mouse key is pressed
        },
        'mouse_not_pressed': {
            # add some methods that are executed when mouse key is not pressed
        }
    },
    'map': {
        'key_pressed': {
            # add some methods that are executed when key is pressed
            pygame.K_w: MoveCameraAction((1.0, 0.0, 0.0)),
            pygame.K_s: MoveCameraAction((-1.0, 0.0, 0.0)),
            pygame.K_d: MoveCameraAction((0.0, 1.0, 0.0)),
            pygame.K_a: MoveCameraAction((0.0, -1.0, 0.0)),
            pygame.K_r: MoveCameraAction((0.0, 0.0, 1.0)),
            pygame.K_q: MoveCameraAction((0.0, 0.0, -1.0)),
            pygame.K_LEFT: TurnYawCameraAction(-1),
            pygame.K_RIGHT: TurnYawCameraAction(1),
            pygame.K_DOWN: TurnPitchCameraAction(-1),
            pygame.K_UP: TurnPitchCameraAction(1),
        },
        'key_not_pressed': {
            # add some methods that are executed when key is not pressed
        },
        'key_down': {
            # add some methods that are executed when key is down pressed
            pygame.K_e: ChangeModeAction("game"),
        },
        'key_up': {
            # add some methods that are executed when key is up pressed
        },
        'mouse_pressed': {
            # add some methods that are executed when mouse key is pressed
        },
        'mouse_not_pressed': {
            # add some methods that are executed when mouse key is not pressed
        }
    }
}
