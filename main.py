import os
import sys
from random import randint
import datetime as dt

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 480
FPS = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

other_data = os.path.join('data', 'others')
sound_start_game = pygame.mixer.Sound(os.path.join(other_data, "button_click.mp3"))
heart = pygame.image.load(os.path.join(other_data, "heart.png"))
heart = pygame.transform.scale(heart, (30, 30))

running = True


def load_image(name, color_key=None):
    fullname = os.path.join(*name)
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


def terminate():
    pygame.quit()
    sys.exit()


class Button:
    def __init__(self, wight, height, color, color_active, button_sound_click):
        self.wight = wight
        self.height = height
        self.color = color
        self.color_active = color_active
        self.button_sound = button_sound_click

    def draw(self, x, y, text, text_size, text_color, text_color_active):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if x < mouse_pos[0] < x + self.wight and y < mouse_pos[1] < y + self.height:
            pygame.draw.rect(screen, self.color_active, (x, y, self.wight, self.height))
            font = pygame.font.Font(None, text_size)
            text_button = font.render(text, True, text_color_active)
            text_x, text_y = x + 10, y + 10
            screen.blit(text_button, (text_x, text_y))
            if mouse_click[0] == 1:
                pygame.mixer.Sound.play(self.button_sound)
                pygame.time.delay(200)
                action = True
                return action
        else:
            pygame.draw.rect(screen, self.color, (x, y, self.wight, self.height))
            font = pygame.font.Font(None, text_size)
            text_button = font.render(text, True, text_color)
            text_x, text_y = x + 10, y + 10
            screen.blit(text_button, (text_x, text_y))


def start_screen():
    fon = pygame.transform.scale(load_image([os.path.join(other_data, 'fon.jpg')]), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Bauhaus 93', 50)
    Title = font.render("Herobyte", 1, (100, 255, 255))
    screen.blit(Title, (20, 10))
    description = '''
    Управление:
    A/D - движение влево/вправо
    Левый шифт - ускорение
    Пробел - прыгать
    Кнопки мыши - атака'''

    font = pygame.font.Font(None, 30)
    text_coord = 40
    for line in description.split('\n'):
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button = Button(250, 70, (70, 130, 180), (70, 50, 255), sound_start_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        start_game = button.draw(410, 130, "Начать игру", 58, (224, 255, 255), (220, 220, 220))
        if start_game:
            return
        pygame.display.flip()
        clock.tick(FPS)


def character_selection_screen():
    intro_text = ["             Выберите своего героя!", ]
    fon = pygame.transform.scale(load_image([os.path.join(other_data, 'character_selection .jpg')]), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button_select = Button(200, 50, (70, 130, 180), (70, 50, 255), sound_start_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        entity = pygame.transform.scale(load_image(['data', 'heroes', 'Entity', 'Entity.png']), (160, 240))
        cat = pygame.transform.scale(load_image(['data', 'heroes', 'Kotik', 'Kotik.png']), (160, 240))
        screen.blit(entity, (150, 100))
        screen.blit(cat, (500, 100))
        button_select_entity = button_select.draw(130, 350, "Выбрать", 58, (224, 255, 255), (220, 220, 220))
        button_select_cat = button_select.draw(480, 350, "Выбрать", 58, (224, 255, 255), (220, 220, 220))
        if button_select_entity:
            return "Entity"
        if button_select_cat:
            return "Kotik"
        pygame.display.flip()
        clock.tick(FPS)


def level_selection_screen():
    fon = pygame.transform.scale(load_image([os.path.join(other_data, 'character_selection .jpg')]), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Выберите уровень", True, (255, 255, 255))
    screen.blit(text, (250, 10))
    button_select = Button(210, 50, (70, 130, 180), (70, 50, 255), sound_start_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        button_select_level_1 = button_select.draw(20, 200, "1 уровень", 58, (224, 255, 255), (220, 220, 220))
        button_select_level_2 = button_select.draw(280, 200, "2 уровень", 58, (224, 255, 255), (220, 220, 220))
        button_select_level_3 = button_select.draw(540, 200, "3 уровень", 58, (224, 255, 255), (220, 220, 220))
        if button_select_level_1:
            return "1"
        elif button_select_level_2:
            return "2"
        elif button_select_level_3:
            return "3"
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(result):
    global score
    if result:
        fon = pygame.transform.scale(load_image([os.path.join(other_data, 'victory_screen.png')]), (WIDTH, HEIGHT))
    else:
        fon = pygame.transform.scale(load_image([os.path.join(other_data, 'game_over_screen.png')]), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(f"очки: {score}", True, (255, 255, 255))
    screen.blit(text, (280, 150))
    button_select = Button(430, 50, (70, 130, 180), (70, 50, 255), sound_start_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        button_menu = button_select.draw(200, 230, "Вернуться в меню", 58, (224, 255, 255), (220, 220, 220))
        button_quit = button_select.draw(200, 310, "Покинуть игру", 58, (224, 255, 255), (220, 220, 220))
        btn_save = button_select.draw(200, 390, "Сохранить результат", 58, (224, 255, 255), (220, 220, 220))
        if button_menu:
            global all_sprites
            all_sprites = pygame.sprite.Group()
            game()
        elif button_quit:
            terminate()
        elif btn_save:
            save_result()
        pygame.display.flip()
        clock.tick(FPS)


def save_result():
    global score, level
    fon = pygame.transform.scale(load_image([os.path.join(other_data, 'character_selection .jpg')]), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    description = '''
        Введите своё имя!
        Нажмите enter чтобы сохранить результат
        '''

    font = pygame.font.Font(None, 40)
    button_select = Button(260, 50, (70, 130, 180), (70, 50, 255), sound_start_game)
    input_text = True
    name = ""
    while True:
        screen.blit(fon, (0, 0))
        text_coord = 40
        for line in description.split('\n'):
            string_rendered = font.render(line, 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_text = False
                    with open(os.path.join('data', 'others', "results.txt"), 'a') as file:
                        time = dt.datetime.now().strftime("%d-%B-%y %H:%M:%S")
                        file.write(f"{name}   {score}   {level}   {time}\n")
                else:
                    if len(name) < 14 and input_text:
                        name += event.unicode
        button_menu = button_select.draw(220, 330, "Вернуться в меню", 40, (224, 255, 255), (220, 220, 220))
        button_quit = button_select.draw(220, 400, "Покинуть игру", 40, (224, 255, 255), (220, 220, 220))
        if button_menu:
            global all_sprites
            all_sprites = pygame.sprite.Group()
            game()
        elif button_quit:
            terminate()
        text_name = font.render(name, True, (255, 255, 255))
        screen.blit(text_name, (200, 200))
        if not input_text:
            font_result = pygame.font.Font(None, 40)
            message = font_result.render("Результат сохранён!", True, (200, 255, 255))
            screen.blit(message, (200, 240))
        pygame.display.flip()


def monster_death(x, y, point, is_alive):
    global score
    font = pygame.font.Font(None, 20)
    text = font.render(str(point), True, (randint(100, 255), randint(100, 255), randint(100, 255)))
    screen.blit(text, (x, y))
    y -= 5
    if is_alive:
        score += 100


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, y, x, fullname):
        super().__init__(all_sprites)
        self.image = load_image([fullname, 'obstacle_' + type + '.png'])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class Weapon(pygame.sprite.Sprite):
    global Enemies

    def __init__(self, x, y, fullname, look):
        super().__init__(all_sprites)
        self.stages = self.cut_sheet(load_image([fullname + '_weapon.png'], -1), (6, 1))
        self.pose = 0
        self.look = look
        self.image = self.stages[self.pose]
        self.rect = self.image.get_rect()

        self.pose = 0
        if not self.look:
            self.image = pygame.transform.flip(self.image, True, False)
            x -= self.rect.w
        self.rect = self.rect.move(x, y)

    def update(self):
        for enemy in Enemies:
            if abs(enemy.rect.x - self.rect.x) <= 30 and abs(enemy.rect.y - self.rect.y) <= 30:
                monster_death(enemy.rect.x, enemy.rect.y, 100, enemy.is_alive)
                enemy.death()
            if enemy.is_dead():
                del Enemies[Enemies.index(enemy)]
                enemy.kill()
        if self.pose == len(self.stages) - 1:
            self.kill()
        self.pose = (self.pose + 1) % len(self.stages)
        self.image = self.stages[self.pose]
        if not self.look:
            self.image = pygame.transform.flip(self.image, True, False)

    def cut_sheet(self, sheet, columns_rows):
        columns, rows = columns_rows
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames


class Entity(pygame.sprite.Sprite):
    global Player, main_map, hero_name, reversed_main_map

    def __init__(self, name, idle, walk, run, jump, death, attack, pos, color_key=0):
        super().__init__(all_sprites)
        self.name = name
        self.is_alive = True
        self.pose = 0
        self.look = 1
        self.y_speed = 0
        self.x_speed = 0
        self.is_falling = False
        self.is_attacking = False
        self.is_moving = False
        self.transformed = False
        self.idle_poses = self.cut_sheet(load_image([name + '_idle.png'], color_key), idle)
        self.walk_poses = self.cut_sheet(load_image([name + '_walk.png'], color_key), walk)
        self.run_poses = self.cut_sheet(load_image([name + '_run.png'], color_key), run)
        self.jump_poses = self.cut_sheet(load_image([name + '_jump.png'], color_key), jump)
        self.death_poses = self.cut_sheet(load_image([name + '_death.png'], color_key), death)
        self.attack_poses = self.cut_sheet(load_image([name + '_attack.png'], color_key), attack)
        self.image = self.idle_poses[self.pose]
        self.rect = self.rect.move(*pos)

    def movement(self, step):
        if self.is_alive and not self.is_attacking:
            y = self.rect.y
            y_to_check = []
            if self.rect.h % 32:
                h_ = self.rect.h // 32 + 1
            else:
                h_ = self.rect.h // 32
            i = 0
            for i in range(h_):
                y_to_check.append(y // 32 + i)
            a = self.rect.h // 32
            if self.rect.h % 32:
                a += 1
            if 32 * a - y % 32 < self.rect.h:
                y_to_check.append(y // 32 + i + 1)
            if not self.is_moving:
                self.is_moving = True
                self.pose = 0
            if not self.is_attacking and not self.is_falling:
                if step > 5 or step < -5:
                    self.pose = (self.pose + 1) % len(self.run_poses)
                    self.image = self.run_poses[self.pose]
                else:
                    self.pose = (self.pose + 1) % len(self.idle_poses)
                    self.image = self.walk_poses[self.pose]
            if step < 0:
                if self.look and not self.is_falling:
                    self.transformed = False
                self.look = 0
            else:
                if not self.look and not self.is_falling:
                    self.transformed = False
                self.look = 1
            if not self.look and not self.transformed:
                self.image = pygame.transform.flip(self.image, True, False)
                self.transformed = True
            step = self.next_x(self.rect.x, y_to_check, step)
            self.rect = self.rect.move(step, 0)
            if step:
                return True
            else:
                return False

    def next_x(self, x, y_, step):
        if x % 32 == 0:
            x_ = x // 32
        else:
            x_ = x // 32 + 1

        for y in y_:
            if self.look:
                line = main_map[y][x_:]
            else:
                line = reversed(main_map[y][:x_ + 1])
            for elem in line:
                if type(elem) == Obstacle:
                    if self.look:
                        dist = elem.rect.x - (x + self.rect.w)
                    else:
                        dist = elem.rect.x + elem.rect.w - x
                    if abs(dist) < abs(step):
                        step = dist
                    break
        return step

    def next_y(self, y, x_, step):
        self.is_falling = True
        if step >= 0:
            for x in x_:
                line = reversed(reversed_main_map[x][:y // 32])
                for elem in line:
                    if type(elem) == Obstacle:
                        dist = y - elem.rect.y - elem.rect.h
                        if dist < step and dist >= 0:
                            step = dist
                        break

        else:
            for x in x_:
                line = reversed_main_map[x][(y + self.rect.h) // 32:]
                for elem in line:
                    if type(elem) == Obstacle:
                        dist = y + self.rect.h - elem.rect.y
                        if dist > step and dist <= 0:
                            step = dist
                        break

        if not step and self.y_speed <= 0:
            self.is_falling = False
        return step

    def jump(self, step):
        if self.is_alive and not self.is_attacking:
            if not self.is_falling:
                self.transformed = False
                self.y_speed = step

    def do_nothing(self):
        self.is_moving = False

    def death(self):
        if self.is_alive:
            self.is_alive = False
            self.pose = -1

    def attack(self):
        if self.is_alive and not self.is_attacking:
            self.pose = 0
            self.is_attacking = True
            if self.look:
                Weapon(self.rect.x + self.rect.w, self.rect.y, self.name, self.look)
            else:
                Weapon(self.rect.x, self.rect.y, self.name, self.look)

    def is_dead(self):
        return all([self.is_alive == False, self.pose == len(self.death_poses) - 1])

    def update(self):
        if self.is_alive and not self.is_attacking:
            self.transformed = False
            if not any([self.is_falling, self.is_attacking, self.is_moving]):
                self.pose = (self.pose + 1) % len(self.idle_poses)
                self.image = self.idle_poses[self.pose]
                if not self.look:
                    self.image = pygame.transform.flip(self.image, True, False)
            x = self.rect.x
            x_to_check = []
            i = 0
            if not self.rect.w // 32:
                x_to_check.append(x // 32)
            for i in range(self.rect.w // 32):
                x_to_check.append(x // 32 + i)
            if 32 - x % 32 < self.rect.w:
                x_to_check.append(x // 32 + i + 1)

            self.y_speed = self.next_y(self.rect.y, x_to_check, self.y_speed - 5)
            if self.is_falling:
                if -10 < self.y_speed <= 10:
                    self.image = self.jump_poses[0]
                elif 10 < self.y_speed <= 20:
                    self.image = self.jump_poses[1]
                elif self.y_speed > 20:
                    self.image = self.jump_poses[2]
                elif -20 <= self.y_speed < -10:
                    self.image = self.jump_poses[3]
                elif self.y_speed < -20:
                    self.image = self.jump_poses[4]

                if not self.look:
                    self.transformed = True
                    self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.rect.move(0, -self.y_speed)
        elif self.is_attacking:
            if self.pose == len(self.attack_poses) - 1:
                self.is_attacking = False
                return
            self.pose = (self.pose + 1) % len(self.attack_poses)
            self.image = self.attack_poses[self.pose]
            if not self.look:
                self.image = pygame.transform.flip(self.image, True, False)

    def cut_sheet(self, sheet, columns_rows):
        columns, rows = columns_rows
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames


class UFO(Entity):
    def __init__(self, name, idle, walk, run, jump, death, pos, attack, color_key):
        super().__init__(name, idle, walk, run, jump, death, pos, attack, color_key)

    def update(self):
        if self.is_alive:
            self.pose = (self.pose + 1) % len(self.walk_poses)
            self.image = self.walk_poses[self.pose]
            if not any([self.is_falling, self.is_attacking, self.is_moving]):
                self.transformed = False
                if not self.look:
                    self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.pose = (self.pose + 1) % len(self.death_poses)
            self.image = self.death_poses[self.pose]

    def jump(self, step):
        if self.is_alive:
            x = self.rect.x
            x_to_check = []
            for i in range(self.rect.w // 32):
                x_to_check.append(x // 32 + i)
            if x % 32 != 0:
                x_to_check.append(x // 32 + i + 1)
            step = self.next_y(self.rect.y, x_to_check, step)
            self.rect = self.rect.move(0, -step)
            if step:
                return True
            return False


def load_level(name):
    fullname = os.path.join('data', 'levels', name, 'level')
    storage = os.path.join('data', 'levels', name)
    with open(fullname, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    player = None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            obj = level_map[y][x]
            if obj != '0':
                if obj in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    obj = Obstacle(obj, y * 32, x * 32, storage)
                elif obj == '@':
                    player = Entity(os.path.join('data', 'heroes', hero_name, hero_name), [4, 1], [6, 1], [6, 1],
                                    [5, 1], [6, 1], [6, 1], [x * 32, y * 32 - 16])
                    obj = None

                elif obj == 'U':
                    enemy = UFO(os.path.join('data', 'enemies', 'UFO', 'UFO'), [6, 1], [6, 1], [6, 1], [2, 1], [6, 1],
                                [6, 1],
                                [x * 32, y * 32], -1)
                    Enemies.append(enemy)

            else:
                obj = None
            level_map[y][x] = obj
    return player, level_map


def find_way(x0, y0, x2, y2):
    global Enemies, Player, main_map, reversed_main_map
    x1, y1 = x0 // 32, y0 // 32
    x2, y2 = x2 // 32, y2 // 32
    ways = [[]]
    i_was = [(x1, y1)]
    coords = [(x1, y1)]
    y_max = len(main_map)
    x_max = len(main_map[0])
    while True:
        go = False
        prev = len(coords)
        for i in range(prev):
            x, y = coords[i]
            if type(main_map[y][x]) != Obstacle:
                way = ways[i]
                if coords[i] == (x2, y2):
                    return way
                if (x, y + 1) not in i_was and y + 1 < y_max:
                    if type(main_map[y + 1][x]) != Obstacle:
                        go = True
                        coords.append((x, y + 1))
                        i_was.append((x, y + 1))
                        ways.append(way + ['d'])

                if (x, y - 1) not in i_was and y - 1 >= 0:
                    if type(main_map[y - 1][x]) != Obstacle:
                        go = True
                        coords.append((x, y - 1))
                        i_was.append((x, y - 1))
                        ways.append(way + ['u'])

                if (x - 1, y) not in i_was and x - 1 >= 0:
                    if type(main_map[y][x - 1]) != Obstacle:
                        go = True
                        coords.append((x - 1, y))
                        i_was.append((x - 1, y))
                        ways.append(way + ['l'])

                if (x + 1, y) not in i_was and x + 1 < x_max:
                    if type(main_map[y][x + 1]) != Obstacle:
                        go = True
                        coords.append((x + 1, y))
                        i_was.append((x + 1, y))
                        ways.append(way + ['r'])

        del coords[:prev]
        del ways[:prev]
        if not go:
            return []


def enemy_live():
    global Enemies, Player, main_map, hero_name, reversed_main_map, number_of_hearts
    prev_x_y = []
    if not Enemies:
        end_screen(True)

    for enemy in Enemies:
        stop = False
        for elem in prev_x_y:
            if (abs(enemy.rect.x - elem[0]) <= 32 and abs(enemy.rect.y - elem[1]) <= 32):
                stop = True
                break
        if not stop:
            way = find_way(enemy.rect.x, enemy.rect.y, Player.rect.x, Player.rect.y)
            if way:
                elem = way[0]
                if elem == 'u':
                    moving = enemy.jump(8)
                    if not moving:
                        if enemy.rect.x >= enemy.rect.w // 2:
                            moving = enemy.movement(-8)
                        else:
                            moving = enemy.movement(8)
                elif elem == 'd':
                    moving = enemy.jump(-8)
                    if not moving:
                        if enemy.rect.x >= enemy.rect.w // 2:
                            moving = enemy.movement(-8)
                        else:
                            moving = enemy.movement(8)
                elif elem == 'l':
                    moving = enemy.movement(-8)
                    if not moving:
                        if enemy.rect.y >= enemy.rect.h // 2:
                            moving = enemy.jump(8)
                        else:
                            moving = enemy.jump(-8)
                elif elem == 'r':
                    moving = enemy.movement(8)
                    if not moving:
                        if enemy.rect.y >= enemy.rect.h // 2:
                            moving = enemy.jump(8)
                        else:
                            moving = enemy.jump(-8)

            if abs(enemy.rect.x - Player.rect.x) <= 30 and abs(enemy.rect.y - Player.rect.y) <= 30 and enemy.is_alive:
                global number_of_hearts
                enemy.death()
                number_of_hearts -= 1
            if enemy.is_dead():
                del Enemies[Enemies.index(enemy)]
                enemy.kill()
            prev_x_y.append([enemy.rect.x, enemy.rect.y])


def drawing_hearts():
    global number_of_hearts, score
    a = 0
    x = 30
    for i in range(number_of_hearts):
        screen.blit(heart, (x, 5))
        x += 40
        a += 1
    if number_of_hearts <= 0:
        end_screen(False)
    font = pygame.font.Font(None, 50)
    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (700, 25))


def game():
    global Enemies, Player, main_map, hero_name, reversed_main_map, number_of_hearts, score, level
    start_screen()
    hero_name = character_selection_screen()
    level = level_selection_screen()
    number_of_hearts = 3
    level = "level_" + level
    Enemies = []
    score = 0
    Player, main_map = load_level(level)
    reversed_main_map = []
    for i in range(len(main_map[0])):
        reversed_main_map.append([])
    for y in range(len(main_map)):
        for x in range(len(main_map[y])):
            reversed_main_map[x].append(main_map[y][x])
    running = True
    while running:
        moving = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Player.jump(50)
            if event.type == pygame.MOUSEBUTTONDOWN:
                Player.attack()
        if pygame.key.get_pressed()[pygame.K_d]:
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                moving = Player.movement(10)
            else:
                moving = Player.movement(5)

        elif pygame.key.get_pressed()[pygame.K_a]:
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                moving = Player.movement(-10)
            else:
                moving = Player.movement(-5)

        if not moving:
            Player.do_nothing()
        enemy_live()
        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        all_sprites.update()
        drawing_hearts()
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


game()
