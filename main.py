import os
import pygame
import random

pygame.init()

FPS = 10
WIDTH = 600  # 25 платформ
HEIGHT = 408  # 17 платформ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
LEVEL = 1

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


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, a_idle, a_walk, a_run, a_jump, a_attack, pos, health, damage):
        super().__init__(all_sprites)
        self.idle_frames = self.cut_sheet(load_image(['heroes', name, name + '_idle.png']), a_idle)
        self.walk_frames = self.cut_sheet(load_image(['heroes', name, name + '_walk.png']), a_walk)
        self.run_frames = self.cut_sheet(load_image(['heroes', name, name + '_run.png']), a_run)
        self.jump_frames = self.cut_sheet(load_image(['heroes', name, name + '_jump.png']), a_jump)
        self.attack_frames = self.cut_sheet(load_image(['heroes', name, name + '_attack1.png']), a_attack)
        self.health = health
        self.damage = damage
        self.falling = False
        self.cur_idle_frame = 0
        self.cur_walk_frame = 0
        self.cur_run_frame = 0
        self.cur_jump_frame = 0
        self.cur_attack_frame = 0
        self.jump_speed = 0
        self.image = self.idle_frames[self.cur_idle_frame]
        self.rect = self.rect.move(*pos)
        self.look = 1
        self.mask = pygame.mask.from_surface(load_image(['heroes', name, name + '.png']))

    def cut_sheet(self, sheet, columns_rows):
        columns, rows = columns_rows
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames

    def go(self, feet):
        if not self.cur_attack_frame and not self.cur_jump_frame:
            self.cur_walk_frame = (self.cur_walk_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.cur_walk_frame]
            if feet > 0:
                self.look = 1
            else:
                self.look = -1
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(feet, 0)
            # while any([pygame.sprite.collide_mask(self, elem) == None for elem in obstacles]):
            #     self.rect = self.rect.move(-1, 0)

    def run(self, feet):
        if not self.cur_attack_frame and not self.cur_jump_frame:
            self.cur_run_frame = (self.cur_run_frame + 1) % len(self.run_frames)
            self.image = self.run_frames[self.cur_run_frame]
            if feet > 0:
                self.look = 1
            else:
                self.look = -1
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(feet, 0)
            # while any([pygame.sprite.collide_mask(self, elem) == None for elem in obstacles]):
            #     self.rect = self.rect.move(-1, 0)

    def attack(self):
        self.cur_attack_frame = (self.cur_attack_frame + 1) % len(self.attack_frames)
        self.image = self.attack_frames[self.cur_attack_frame]
        if self.look == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self, k_down=False):
        if not self.cur_attack_frame:
            if self.falling and k_down:
                return
            elif k_down:
                self.jump_speed = 60
            self.jump_speed -= 10
            self.cur_jump_frame = (self.cur_jump_frame + 1) % len(self.jump_frames)
            self.image = self.jump_frames[self.cur_jump_frame]
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(10 * self.look, -self.jump_speed)
        elif self.cur_attack_frame:
            self.attack()

    def update(self):
        if not self.cur_attack_frame and not self.cur_jump_frame:
            self.cur_idle_frame = (self.cur_idle_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.cur_idle_frame]
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        elif self.cur_attack_frame:
            self.attack()
        elif self.cur_jump_frame:
            self.jump()

        if all([pygame.sprite.collide_mask(self, elem) == None for elem in obstacles]):
            self.rect = self.rect.move(0, 24)
            if not all([pygame.sprite.collide_mask(self, elem) == None for elem in obstacles]):
                while not all([pygame.sprite.collide_mask(self, elem) == None for elem in obstacles]):
                    self.rect = self.rect.move(0, -1)
                self.rect = self.rect.move(0, 1)
            self.falling = True
        else:
            self.falling = False


class Player(Entity):
    def __init__(self, name, a_idle, a_walk, a_run, a_jump, a_attack, pos, health, damage):
        super().__init__(name, a_idle, a_walk, a_run, a_jump, a_attack, pos, health, damage)

def load_level(filename):
    filename = os.path.join('data', *filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return [list(elem) for elem in level_map]


class Platform(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(all_sprites)
        self.image = load_image(
            ['levels', 'level_' + str(LEVEL), 'platform_' + str(type) + '.png'])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x * 24, y * 24)


class Level:
    def __init__(self, level_map):
        self.level_map = load_level(level_map)
        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[0])):
                if self.level_map[y][x] == '1' or self.level_map[y][x] == '2':
                    obstacles.append(Platform(self.level_map[y][x], x, y))
                elif self.level_map[y][x] == '@':
                    global player
                    player = Player(random.choice(players), [4, 1], [6, 1], [6, 1], [6, 1], [6, 1], [y * 24, x * 24 - 23], 100, 25)

obstacles = []
players = ['Woodcutter', 'GraveRobber', 'SteamMan']
player = None
level_1 = Level(['levels', 'level_1', 'main_map.txt'])
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attack()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(True)
    if pygame.key.get_pressed()[pygame.K_d]:
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            player.run(10)
        else:
            player.go(5)
    if pygame.key.get_pressed()[pygame.K_a]:
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            player.run(-10)
        else:
            player.go(-5)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
