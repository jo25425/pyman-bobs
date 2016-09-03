import pygame_sdl2 as pygame
from helpers import load_image


class Booster(pygame.sprite.Sprite):

    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('dot_magenta.png', -1)

        if rect is not None:
            self.rect = rect
