import os
import pygame

pygame.init()

FPS = 10
WIDTH = 600
HEIGHT = 400
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


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet_calm, sheet_walk, sheet_run, sheet_attack,
                 columns_calm, rows_calm,
                 columns_walk, rows_walk,
                 columns_run, rows_run,
                 columns_attack, rows_attack, x, y):
        super().__init__(all_sprites)
        self.calm_frames = self.cut_sheet(sheet_calm, columns_calm, rows_calm)
        self.walk_frames = self.cut_sheet(sheet_walk, columns_walk, rows_walk)
        self.run_frames = self.cut_sheet(sheet_run, columns_run, rows_run)
        self.attack_frames = self.cut_sheet(sheet_attack, columns_attack, rows_attack)
        self.cur_calm_frame = 0
        self.cur_walk_frame = 0
        self.cur_run_frame = 0
        self.cur_attack_frame = 0
        self.image = self.calm_frames[self.cur_calm_frame]
        self.rect = self.rect.move(x, y)
        self.look = 1

    def cut_sheet(self, sheet, columns, rows):
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames

    def go(self, feet):
        if not self.cur_attack_frame:
            self.cur_calm_frame = 0
            self.cur_run_frame = 0
            self.cur_attack_frame = 0
            self.cur_walk_frame = (self.cur_walk_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.cur_walk_frame]
            if feet > 0:
                self.look = 1
            else:
                self.look = -1
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(feet, 0)
        else:
            self.attack()

    def run(self, feet):
        if not self.cur_attack_frame:
            self.cur_run_frame = (self.cur_run_frame + 1) % len(self.run_frames)
            self.image = self.run_frames[self.cur_run_frame]
            if feet > 0:
                self.look = 1
            else:
                self.look = -1
            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(feet, 0)
        else:
            self.attack()

    def attack(self):
        self.cur_attack_frame = (self.cur_attack_frame + 1) % len(self.attack_frames)
        self.image = self.attack_frames[self.cur_attack_frame]
        if self.look == -1:
            self.image = pygame.transform.flip(self.image, True, False)


    def update(self):
        if not self.cur_attack_frame:
            self.cur_calm_frame = (self.cur_calm_frame + 1) % len(self.calm_frames)
            self.image = self.calm_frames[self.cur_calm_frame]

            if self.look == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.attack()


running = True
player = Player(load_image(['heroes', '1 Woodcutter', 'Woodcutter_idle.png']),
                load_image(['heroes', '1 Woodcutter', 'Woodcutter_walk.png']),
                load_image(['heroes', '1 Woodcutter', 'Woodcutter_run.png']),
                load_image(['heroes', '1 Woodcutter', 'Woodcutter_attack3.png']), 4, 1, 6, 1, 6, 1, 6, 1, 50, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attack()
    if pygame.key.get_pressed()[pygame.K_d]:
        if pygame.key.get_pressed()[pygame.K_LSHIFT ]:
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
