'''
//TODO
[X] Limit movement to window bounds
[X] Add speed booster, lower default speed, back to normal after countdown
[ ] Add obstacles: collision that prevents movement rather than kills object
[ ] Make snake face other way when going right vs. left
[ ] Nicer text: reserved area with frame and nicer colour scheme
[ ] Add second player
'''

import sys
import random
import pygame_sdl2 as pygame
from pygame_sdl2 import locals
from Snake import Snake
from Pellet import Pellet
from Booster import Booster

if not pygame.font:
    print('Warning: Pygame fonts disabled.')
if not pygame.mixer:
    print('Warning: Pygame sounds disabled.')

# Constants
BOOSTER_DURATION = 5
BOOSTER_STRENGTH = 3


class PyMan:
    '''The main PyMan class: This class handles the initialisation and creating
    of the game'''

    def __init__(self, width=640, height=480):
        pygame.init()

        self.width = width
        self.height = height

        # Create the screen
        # set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.snake = Snake()

    def go(self):
        '''This is the main game method'''
        self.load_sprites()

        # Define keystroke event delay and interval
        # pygame.key.set_repeat(500, 30)

        # Create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # Define font
        if pygame.font:
            font = pygame.font.Font(None, 36)

        move_keys = [locals.K_RIGHT, locals.K_LEFT, locals.K_UP, locals.K_DOWN]

        # The main game loop contains all in-game actions
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Keyboard input handling
            pressed = pygame.key.get_pressed()
            pressed_move_keys = [key for key in move_keys if pressed[key]]
            if pressed_move_keys:
                self.snake.move(pressed_move_keys)

            # Collision handling
            self.handle_collisions()

            # Rendering
            self.render(font)

    def handle_collisions(self):
        # collide_rect_ratio(ratio) -> collided_callable
        # Check collision with scaled versions of sprites rect attributes
        collided_callable = pygame.sprite.collide_rect_ratio(0.5)
        # spritecollide(sprite, group, dokill, collided=None)

        # Collisions with pellets
        collisions = pygame.sprite.spritecollide(self.snake,
                                                 self.pellet_sprites,
                                                 True,
                                                 collided_callable)
        self.snake.pellets += len(collisions)

        # Collisions with boosters
        collisions = pygame.sprite.spritecollide(self.snake,
                                                 self.booster_sprites,
                                                 True,
                                                 collided_callable)
        if collisions:
            self.snake.start_boost(BOOSTER_STRENGTH, BOOSTER_DURATION)

    def render(self, font):
        self.screen.blit(self.background, (0, 0))
        self.pellet_sprites.draw(self.screen)
        self.booster_sprites.draw(self.screen)
        self.snake_sprites.draw(self.screen)

        if pygame.font:
            text = font.render('Pellets {}'.format(self.snake.pellets),
                               1, (255, 0, 0))
            text_pos = text.get_rect(centerx=self.width / 2)
            self.screen.blit(text, text_pos)

        pygame.display.flip()

    def load_sprites(self):
        # Snake
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

        item_width, item_height = 64, 64
        n_horizontal = int(self.width / item_width)
        n_vertical = int(self.height / item_height)

        # Pellets
        self.pellet_sprites = pygame.sprite.Group()

        # Boosters
        self.booster_sprites = pygame.sprite.Group()

        for x in range(n_horizontal):
            for y in range(n_vertical):
                r = pygame.Rect(x * item_width, y * item_height,
                                item_width, item_height)
                if random.random() < 0.9:
                    self.pellet_sprites.add(Pellet(r))
                else:
                    self.booster_sprites.add(Booster(r))


if __name__ == '__main__':
    MainWindow = PyMan()
    MainWindow.go()
