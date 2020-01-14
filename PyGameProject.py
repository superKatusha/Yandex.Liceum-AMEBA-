# -*- coding: utf-8 -*-
import pygame
import os
import sys
import math
import random


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def press_detect(pos, button):
    x = pos[0]
    y = pos[1]
    if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
        return True
    else:
        return False


def start_screen():
    intro_text = ["Mini Mario"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = [275, 90]
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - (line_rect[2] // 2), text_coord[1]])
        text_coord[1] += line_rect[3] + 30
    screen.blit(font.render('ВВЕДИТЕ НАЗВАНИЕ КАРТЫ', 1, (0, 0, 0)), [20, 300])
    pygame.draw.rect(screen, (255, 255, 255), [125, 350, 300, 40])
    screen.blit(font.render(a, 1, (0, 0, 0)), [130, 350])


class Window:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.map = []
        self.map_size = []
        self.block_size = 0
        self.hero_height = 0
        self.hero_width = 0
        self.bul_size = 10
        self.enemy_height = 0
        self.enemy_width = 0

    def input_map(self, name):
        self.map = []
        fullname = os.path.join('maps', name)
        with open(fullname, 'r') as in_file:
            a = in_file.readlines()
        for i in range(len(a)):
            if i == 0:
                self.map_size = list(map(int, a[i].split()))
            else:
                self.map.append(list(a[i].rstrip().ljust(self.map_size[0], '.')))
        self.block_size = self.width // self.map_size[0]
        self.hero_height = int(round(1 * self.block_size))
        self.hero_width = int(round(0.7 * self.block_size))
        self.enemy_height = self.hero_height
        self.enemy_width = self.hero_width

    def render(self):
        if menu:
            start_screen()
        else:
            for i in range(self.map_size[1]):
                for j in range(self.map_size[0]):
                    if self.map[i][j] == '.':
                        screen.blit(pygame.transform.scale(sprites['grass'],
                                                           (self.block_size, self.block_size)),
                                    [i * self.block_size, j * self.block_size])
                    if self.map[i][j] == '~':
                        screen.blit(pygame.transform.scale(sprites['water'],
                                                           (self.block_size, self.block_size)),
                                    [i * self.block_size, j * self.block_size])
                    elif self.map[i][j] == '#':
                        screen.blit(pygame.transform.scale(sprites['box'],
                                                           (self.block_size, self.block_size)),
                                    [i * self.block_size, j * self.block_size])
                    elif self.map[i][j] == '0':
                        screen.blit(pygame.transform.scale(sprites['black'],
                                                           (self.block_size, self.block_size)),
                                    [i * self.block_size, j * self.block_size])
            screen.blit(pygame.transform.scale(sprites['trader'],
                                            (self.hero_width, self.hero_height)),
                        [trader.x, trader.y])
            screen.blit(pygame.transform.scale(sprites['hero'],
                                               (self.hero_width, self.hero_height)),
                        hero.get_pos())
            for bullet in bullets:
                screen.blit(pygame.transform.scale(sprites['box'],
                                                   (self.bul_size, self.bul_size)),
                            [bullet.x, bullet.y])
            for enemy in enemies:
                screen.blit(pygame.transform.scale(sprites['enemy'],
                                                   (self.enemy_width, self.enemy_height)),
                            [enemy.x, enemy.y])


def collision(ent, x, y):
    [x1, y1, width, height] = ent.get_rect()
    x1 += x
    x2 = x1 + width
    y1 += y
    y2 = y1 + height
    if (window.map[int(x1 // window.block_size)][int(y1 // window.block_size)] == '#' or
            window.map[int(x2 // window.block_size)][int(y2 // window.block_size)] == '#'):
        return 'Wall'
    for entity in entities:
        if entity != ent:
            [x21, y21, width2, height2] = entity.get_rect()
            x22 = x21 + width2
            y22 = y21 + height2
            if ((x2 >= x21 >= x1 and y2 >= y21 >= y1) or
                    (x2 >= x22 >= x1 and y2 >= y21 >= y1) or
                    (x2 >= x21 >= x1 and y2 >= y22 >= y1) or
                    (x2 >= x22 >= x1 and y2 >= y22 >= y1)):
                return entity
    return 'False'


class Entity:
    def __init__(self, rect, name):
        [self.x_pos, self.y_pos, self.width, self.height] = rect
        self.name = name

    def get_rect(self):
        return [self.x_pos, self.y_pos, self.width, self.height]

    def move(self, x, y):
        self.x_pos += x
        self.y_pos += y

    def delete(self):
        self.delete()


class Trader(Entity):
    def __init__(self):
        for i in range(window.map_size[1]):
            for j in range(window.map_size[0]):
                if window.map[i][j] == 'T':
                    self.x = j * window.block_size + window.block_size - window.hero_width // 2
                    self.y = i * window.block_size
                    window.map[i][j] = '.'
                    break

    def get_pos(self):
        return [self.x, self.y]


class Hero(Entity):
    def __init__(self):
        self.hp = 10
        for i in range(window.map_size[1]):
            for j in range(window.map_size[0]):
                if window.map[i][j] == '@':
                    self.x = j * window.block_size + window.block_size - window.hero_width // 2
                    self.y = i * window.block_size
                    window.map[i][j] = '.'
                    break
        super().__init__([self.x, self.y + 0.7 * window.hero_height, window.hero_width, 0.3 * window.hero_height], 'Hero')

    def move(self, x, y):
        dx = x
        dy = y
        if 0 <= self.x + dx <= window.width - window.block_size:
            if collision(self, dx, dy) == 'False':
                self.x += dx
            else:
                dx = 0
        if 0 <= self.y + dy <= window.height - window.block_size:
            if collision(self, dx, dy) == 'False':
                self.y += dy
            else:
                dy = 0
        super().move(dx, dy)

    def get_pos(self):
        return [self.x, self.y]


class Bullet(Window):
    def __init__(self, delt, cords, speed):
        [self.dx, self.dy] = delt
        [self.x, self.y] = cords
        self.speed = speed
        self.a = True

    def move(self):
        if self.collision():
            self.x += self.speed * self.dx
            self.y += self.speed * self.dy
        else:
            self.a = False

    def get_pos(self):
        return [self.x, self.y]

    def collision(self):
        x1 = int((self.x + self.speed * self.dx) // window.block_size)
        x2 = int((self.x + self.speed * self.dx + window.bul_size) // window.block_size)
        y1 = int((self.y + self.speed * self.dy) // window.block_size)
        y2 = int((self.y + self.speed * self.dy + window.bul_size) // window.block_size)
        #print(x1, x2, y1, y2)
        if (window.map[x1][y1] != '#' and window.map[x2][y1] != '#'
                and window.map[x1][y2] != '#' and window.map[x2][y2]):
            return True
        return False


class Enemy(Entity):
    def __init__(self, x, y, hp):
        self.hp = hp
        self.speed = 1
        self.x = x
        self.y = y
        super().__init__([self.x, self.y + 0.7 * window.enemy_height, window.enemy_width, 0.3 * window.enemy_height],
                         'Enemy')

    def move(self):
        deleted_bullets = []
        for i in range(len(bullets)):
            bulleter = bullets[i].get_pos()
            if round(bulleter[0]) in range(round(self.x), round(self.x) + 40) and round(bulleter[1]) in range(round(self.y), round(self.y) + 40):
                damaged_sound1.play()
                deleted_bullets.append(i)
                self.hp -= 20
        deleted_bullets = sorted(deleted_bullets)
        for _ in deleted_bullets:
            del bullets[_]
        destination = hero.get_pos()
        dx = destination[0] - self.x
        dy = destination[1] - self.y
        if dy != 0 and dx != 0:
            k = math.atan(dx / dy)
            if destination[1] - self.y < 0:
                dx, dy = -math.sin(k), -math.cos(k)
            else:
                dx, dy = math.sin(k), math.cos(k)
        elif dx == 0 and dy > 0:
            dx, dy = 0, 1
        elif dy == 0 and dx > 0:
            dx, dy = 1, 0
        if 0 <= self.x + dx <= window.width - window.block_size:
            if collision(self, dx, dy) == 'False':
                self.x += dx
            else:
                dx = 0
        if 0 <= self.y + dy <= window.height - window.block_size:
            if collision(self, dx, dy) == 'False':
                self.y += dy
            else:
                dy = 0
        super().move(dx, dy)
        if self.hp < 1:
            enemies.remove(self)
            entities.remove(self)


pygame.init()
a = ''
FPS = 60
size = width, height = 550, 550
sprites = {'grass': load_image('grass.png'), 'hero': load_image('skin2.png'),
           'box': load_image('box.png'), 'trader': load_image('trader.png'),
           'black': load_image('black.jpg'), 'enemy': load_image('skin1.png'),
           'water': load_image('water.png')}
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
shoot_sound1 = pygame.mixer.Sound('sounds/shot_1.wav')
damaged_sound1 = pygame.mixer.Sound('sounds/damaged.wav')
move_sound1 = pygame.mixer.Sound('sounds/move_hero.wav')
bullets = []
enemies = []
entities = []
screen = pygame.display.set_mode(size)
window = Window(size)
running = True
menu = True
move_left, move_right, move_up, move_down = False, False, False, False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if menu:
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    if os.path.exists(os.path.join('maps', a + '.txt')):
                        window.input_map(a + '.txt')
                        menu = False
                        hero = Hero()
                        trader = Trader()
                        for i in range(window.map_size[1]):
                            for j in range(window.map_size[0]):
                                if window.map[i][j] == '-':
                                    x = j * window.block_size + window.block_size - window.enemy_width // 2
                                    y = i * window.block_size
                                    window.map[i][j] = '.'
                                    enemies.append(Enemy(x, y, 100))
                        entities = [hero, *enemies]

                    else:
                        print('несуществующая карта')
                        terminate()
                elif event.key == pygame.K_BACKSPACE:
                    if len(a) != 0:
                        a = a[:-1]
                else:
                    a += chr(event.key)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_d:
                    move_right = True
                elif event.key == pygame.K_w:
                    move_up = True
                elif event.key == pygame.K_s:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_w:
                    move_up = False
                elif event.key == pygame.K_s:
                    move_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shoot_sound1.play()
                    speed = 4
                    destination = list(event.pos)
                    cords = [hero.get_pos()[0] + window.hero_width // 2,
                             hero.get_pos()[1] + window.hero_height // 2]
                    dx = destination[0] - cords[0]
                    dy = destination[1] - cords[1]
                    if dy != 0 and dx != 0:
                        k = math.atan(dx / dy)
                        if destination[1] - cords[1] < 0:
                            dx, dy = -math.sin(k), -math.cos(k)
                        else:
                            dx, dy = math.sin(k), math.cos(k)
                    elif dx == 0:
                        dx, dy = 0, 1
                    elif dy == 0:
                        dx, dy = 1, 0
                    bullets.append(Bullet([dx, dy], cords, speed))
    if move_left:
        channel1.play(move_sound1)
        hero.move(-2, 0)
    elif move_right:
        channel1.play(move_sound1)
        hero.move(2, 0)
    if move_up:
        channel1.play(move_sound1)
        hero.move(0, -2)
    elif move_down:
        channel1.play(move_sound1)
        hero.move(0, 2)
    for bullet in bullets:
        bullet.move()
        if not bullet.a:
            bullets.remove(bullet)
    for enemy in enemies:
        enemy.move()
    screen.fill((0, 0, 0))
    window.render()
    pygame.display.flip()
    clock.tick(FPS)
