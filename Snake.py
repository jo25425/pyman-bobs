import threading
import pygame_sdl2 as pygame
from pygame_sdl2 import locals
from helpers import load_image, is_within_bounds

# Constants
SPEED = 2


class Snake(pygame.sprite.Sprite):
    '''This is the snake that moves around the screen'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('snake.png', -1)
        self.pellets = 0
        self.speed = SPEED
        self.radius = 20
        self.boost = None

    def move(self, keys):
        '''Move in one of the four standard directions'''
        x_move, y_move = 0, 0

        if locals.K_RIGHT in keys:
            x_move += self.speed
        if locals.K_LEFT in keys:
            x_move += -self.speed
        if locals.K_UP in keys:
            y_move += -self.speed
        if locals.K_DOWN in keys:
            y_move += self.speed

        if is_within_bounds(self.rect.copy().move(x_move, y_move)):
            self.rect.move_ip(x_move, y_move)

    def unboost(self):
        self.speed = SPEED
        self.boost = None

    def start_boost(self, strength, duration):
        if self.boost is None:
            self.speed *= strength
        else:
            self.boost.cancel()
        self.boost = threading.Timer(duration, self.unboost)
        self.boost.start()
