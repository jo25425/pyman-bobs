'''
//TODO
[X] Limit movement to window bounds
[X] Add speed booster, lower default speed, back to normal after countdown
[X] Render initial world as grid from array
[ ] Add obstacles: collision that prevents movement rather than kills object
[ ] Place obstacles from maps
[ ] Add new prizes with different values (fruit? mice?)
[ ] Make snake face other way when going right vs. left
[ ] Nicer text: reserved area with frame and nicer colour scheme
[ ] Add second player / enemies (AI)
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
GRID_SPACING = 64
GRID_COLOR = (255, 255, 0)
GRID_THICKNESS = 1.5
MOVE_KEYS = [
    locals.K_RIGHT,
    locals.K_LEFT,
    locals.K_UP,
    locals.K_DOWN
]


class PyMan:
    '''The main PyMan class: This class handles the initialisation and creating
    of the game'''

    def __init__(self, width=640, height=512):
        pygame.init()

        self.width = width
        self.height = height
        self.grid = [[0 for x in range(int(self.width / GRID_SPACING))]
                     for y in range(int(self.height / GRID_SPACING))]

        # Create the screen
        # set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.snake = Snake()

    def go(self):
        '''This is the main game method'''
        self.load_map()
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

        # The main game loop contains all in-game actions
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Keyboard input handling
            pressed = pygame.key.get_pressed()
            pressed_move_keys = [key for key in MOVE_KEYS if pressed[key]]
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

        self.draw_grid()

        self.pellet_sprites.draw(self.screen)
        self.booster_sprites.draw(self.screen)
        self.snake_sprites.draw(self.screen)

        if pygame.font:
            text = font.render('Pellets {}'.format(self.snake.pellets),
                               1, (255, 0, 0))
            text_pos = text.get_rect(centerx=self.width / 2)
            self.screen.blit(text, text_pos)

        pygame.display.flip()

    def load_map(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if random.random() < 0.9:
                    self.grid[i][j] = 'P'
                else:
                    self.grid[i][j] = 'B'

    def draw_grid(self):
        closed = False

        for i in range(1, len(self.grid)):
            points = [(0, i * GRID_SPACING), (self.width, i * GRID_SPACING)]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)
        for j in range(1, len(self.grid[i])):
            points = [(j * GRID_SPACING, 0), (j * GRID_SPACING, self.width)]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)

    def load_sprites(self):
        # Snake
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

        # Pellets, boosters
        self.pellet_sprites = pygame.sprite.Group()
        self.booster_sprites = pygame.sprite.Group()

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                r = pygame.Rect(j * GRID_SPACING, i * GRID_SPACING,
                                GRID_SPACING, GRID_SPACING)
                if self.grid[i][j] == 'P':
                    self.pellet_sprites.add(Pellet(r))
                elif self.grid[i][j] == 'B':
                    self.booster_sprites.add(Booster(r))


if __name__ == '__main__':
    MainWindow = PyMan()
    MainWindow.go()
