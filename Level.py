import os
import sys

import pygame

LEVEL = 1
pygame.init()

FPS = 10
WIDTH = 600  # 25 платформ
HEIGHT = 408  # 17 платформ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', *name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join('data', *filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return [list(elem) for elem in level_map]


class Platform(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(all_sprites)
        self.image = load_image(
            ['levels', 'level_' + str(LEVEL), 'platform_' + '_'.join([str(LEVEL), str(type)]) + '.png'])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * 24, y * 24)


class Level:
    def __init__(self, level_map):
        self.level_map = load_level(level_map)
        for y in range(17):
            for x in range(25):
                if int(self.level_map[y][x]):
                    Platform(self.level_map[y][x], x, y)


pygame.display.set_caption('Десант')
level_1 = Level(['levels', 'level_1', 'main_level_1.txt'])
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
