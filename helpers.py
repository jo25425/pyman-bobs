import os
import pygame_sdl2 as pygame


def is_within_bounds(rect):
    w, h = pygame.display.get_surface().get_size()
    return 0 <= rect.x <= w - rect.w and 0 <= rect.y <= h - rect.h


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        print('Cannot load image:', name)
        raise SystemExit(err)

    image = image.convert_alpha()

    # Just using alpha from png for now as I couldn't get this to work
    # image = image.convert()
    # if colorkey is not None:
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey, locals.RLEACCEL)

    return image, image.get_rect()
