import pygame
import settings

from action import DoneAction
from translator import Translator
from world import World
from coords import CoordConverter
from render import Renderer

clock = pygame.time.Clock()
pygame.init()

# pygame.display.init()  # initialization of display
display = (1000,1000)  # display
screen = pygame.display.set_mode(display)
surface = pygame.Surface(display)

scale = (1,1)
world = World()
render = Renderer(screen, ((0,0), display), scale)

def main_loop():
    translator = Translator(settings.TRANSLATION_MAP, DoneAction())

    def collect_actions():
        result = translator.translate_pressed(world.mode)
        for event in pygame.event.get():
            result += translator.translate_event(world.mode, event)
        return result

    while True:
        world.setup(render.coords)

        actions = collect_actions()

        if any(action.is_done() for action in actions):
            break

        for action in actions:
            action.change_world(world, render)

        world.update()

        render.update(world)
        pygame.display.flip()

        clock.tick(settings.FPS)


if __name__ == "__main__":
    main_loop()
    pygame.quit()
