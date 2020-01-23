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
    intro_text = ["ROGALIC"]
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


def indicators():
    intro_text = [str(hp)]
    font = pygame.font.Font(None, 35)
    text_coord = [105, 548]
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - (line_rect[2] // 2), text_coord[1]])
        text_coord[1] += line_rect[3] + 30
    screen.blit(pygame.transform.scale(sprites['hp'],
                                       (30, 30)),
                [150, 545])
    if type(inventory[active]) in [Weapon, Staff]:
        intro_text = [str(ammo[inventory[active].ammo])]
        font = pygame.font.Font(None, 35)
        text_coord = [105, 578]
        for line in intro_text:
            string_rendered = font.render(line, 1, (255, 0, 0))
            line_rect = string_rendered.get_rect()
            screen.blit(string_rendered, [text_coord[0] - (line_rect[2] // 2), text_coord[1]])
            text_coord[1] += line_rect[3] + 30
        screen.blit(pygame.transform.scale(sprites['bull'],
                                           (50, 30)),
                    [140, 575])


def draw_inventory():
    screen.blit(pygame.transform.scale(sprites['inventory'],
                                       (150, 650)),
                [400, 0])
    for i in range(len(inventory)):
        if inventory[i] != 0:
            name = inventory[i].name
            if i < 3:
                screen.blit(pygame.transform.scale(sprites[name], (37, 37)),
                            [409 + 46 * i, 207])
            else:
                y = 10 + 44 * ((i - 3) // 3)
                x = 409 + 47 * (i % 3)
                screen.blit(pygame.transform.scale(sprites[inventory[i].name], (37, 37)),
                            [x, y])
    if grab:
        cords = pygame.mouse.get_pos()
        screen.blit(pygame.transform.scale(sprites[grab_item.name], (37, 37)),
                    [cords[0] + dx, cords[1] + dy])


def collision(ent, x, y):
    damage = 0
    if ent.name == 'enemy':
        for bullet in bullets:
            x1, y1 = ent.get_pos()
            x2, y2 = x1 + ent.width, y1 + ent.height
            [x21, y21] = bullet.get_pos()
            x22, y22 = x21 + 7, y21 + 7
            if ((x2 >= x21 >= x1 and y2 >= y21 >= y1) or
                (x2 >= x22 >= x1 and y2 >= y21 >= y1) or
                (x2 >= x21 >= x1 and y2 >= y22 >= y1) or
                (x2 >= x22 >= x1 and y2 >= y22 >= y1)):
                damage += bullet.dmg
                bullets.remove(bullet)
    [x1, y1, width, height] = ent.get_rect()
    x1 += x
    x2 = x1 + width
    y1 += y
    y2 = y1 + height
    map_x1 = int(x1 // window.block_size)
    map_x2 = int(x2 // window.block_size)
    map_y1 = int(y1 // window.block_size)
    map_y2 = int(y2 // window.block_size)
    # print('x1y1: {}'.format(window.map[map_y1][map_x1]))
    # print('x2y1: {}'.format(window.map[map_y1][map_x2]))
    # print('x1y2: {}'.format(window.map[map_y2][map_x1]))
    # print('x2y2: {}'.format(window.map[map_y2][map_x2]))
    if (window.map[map_y1][map_x1] in '#=' or
            window.map[map_y1][map_x2] in '#=' or
            window.map[map_y2][map_x1] in '#=' or
            window.map[map_y2][map_x2] in '#='):
        return ['Wall', damage]
    for entity in entities:
        if entity != ent:
            [x21, y21, width2, height2] = entity.get_rect()
            x22 = x21 + width2
            y22 = y21 + height2
            if ((x2 >= x21 >= x1 and y2 >= y21 >= y1) or
                    (x2 >= x22 >= x1 and y2 >= y21 >= y1) or
                    (x2 >= x21 >= x1 and y2 >= y22 >= y1) or
                    (x2 >= x22 >= x1 and y2 >= y22 >= y1) or
                    (x22 >= x1 >= x21 and y22 >= y1 >= y21) or
                    (x22 >= x2 >= x21 and y22 >= y2 >= y21) or
                    (x22 >= x1 >= x21 and y22 >= y2 >= y21) or
                    (x22 >= x2 >= x21 and y22 >= y1 >= y21)):
                return [entity.name, damage]
    if ent.name == 'hero':
        if (window.map[map_y1][map_x1] == 'd' and
                window.map[map_y1][map_x2] == 'd' and
                window.map[map_y2][map_x1] == '.' and
                window.map[map_y2][map_x2] == '.'):
            return ['DoorD']
        elif (window.map[map_y1][map_x1] == '.' and
                window.map[map_y1][map_x2] == '.' and
                window.map[map_y2][map_x1] == 'd' and
                window.map[map_y2][map_x2] == 'd'):
            return ['DoorU']
        elif (window.map[map_y1][map_x1] == 'd' and
                window.map[map_y1][map_x2] == '.' and
                window.map[map_y2][map_x1] == 'd' and
                window.map[map_y2][map_x2] == '.'):
            return ['DoorR']
        elif (window.map[map_y1][map_x1] == '.' and
                window.map[map_y1][map_x2] == 'd' and
                window.map[map_y2][map_x1] == '.' and
                window.map[map_y2][map_x2] == 'd'):
            return ['DoorL']
    if (window.map[map_y1][map_x1] == 'D' or
            window.map[map_y1][map_x2] == 'D' or
            window.map[map_y2][map_x1] == 'D' or
            window.map[map_y2][map_x2] == 'D'):
        return ['Door', damage]
    return ['False', damage]


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Window:
    def __init__(self, size):
        global entities
        self.width = size[0]
        self.height = size[1]
        self.map = []
        self.map_size = []
        self.block_size, self.old_block_size, self.scale = 0, 0, 0
        self.bul_size = 7
        self.room_x, self.room_y, self.room_width, self.room_height = 0, 0, 0, 0
        self.dx, self.dy = 0, 0

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

    def render(self):
        global hp, bullets_count
        if menu:
            start_screen()  # меню игры
        else:
            indicators()  # отрисовка индикаторов (хп, патроны и т.д.)
            en = []
            for enemy in enemies:
                if (self.room_x + self.room_width > enemy.x // window.block_size > self.room_x - 1 and
                        self.room_y + self.room_height > enemy.y // window.block_size > self.room_y - 1):
                    en.append(enemy)
            # отрисовка карты
            for i in range(self.room_y, self.room_y + self.room_height + 1):
                for j in range(self.room_x, self.room_x + self.room_width + 1):
                    if self.map[i][j] == '.':
                        screen.blit(pygame.transform.scale(sprites['grass'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
                    elif self.map[i][j] in 'dD':
                        screen.blit(pygame.transform.scale(sprites['grass'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
                        if len(en) == 0:
                            self.map[i][j] = 'd'
                            screen.blit(pygame.transform.scale(sprites['open_door'],
                                                               (self.x, self.x)),
                                        [self.dx + j * self.x, self.dy + i * self.x])
                        else:
                            self.map[i][j] = 'D'
                            screen.blit(pygame.transform.scale(sprites['closed_door'],
                                                               (self.x, self.x)),
                                        [self.dx + j * self.x, self.dy + i * self.x])
                    elif self.map[i][j] == '~':
                        screen.blit(pygame.transform.scale(sprites['water'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
                    elif self.map[i][j] in '#=':
                        screen.blit(pygame.transform.scale(sprites['box'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
                    elif self.map[i][j] in 'c':
                        screen.blit(pygame.transform.scale(sprites['grass'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
                        screen.blit(pygame.transform.scale(sprites['chest'],
                                                           (self.x, self.x)),
                                    [self.dx + j * self.x, self.dy + i * self.x])
            for entity in entities:
                # отрисовка всех существ на карте
                if ((self.room_x + self.room_width > entity.x // window.block_size > self.room_x - 1 and
                        self.room_y + self.room_height > entity.y // window.block_size > self.room_y - 1) or
                        entity.name == 'hero'):
                    # отрисовка предмета в руках героя
                    if inventory[active] != 0 and entity.name == 'hero':
                        screen.blit(pygame.transform.scale(sprites[entity.name].image,
                                                           (int(entity.width * self.scale),
                                                            int(entity.height * self.scale))),
                                    [self.dx + entity.x, self.dy + entity.y])
                        screen.blit(pygame.transform.scale(sprites[inventory[active].name],
                                                           (int(entity.height * self.scale * 0.85),
                                                            int(entity.height * self.scale * 0.85))),
                                    [self.dx + entity.x, self.dy + entity.y + 10])
                    else:
                        if type(sprites[entity.name]) is AnimatedSprite:
                            screen.blit(pygame.transform.scale(sprites[entity.name].image,
                                                               (int(entity.width * self.scale),
                                                                int(entity.height * self.scale))),
                                        [self.dx + entity.x, self.dy + entity.y])
                        else:
                            screen.blit(pygame.transform.scale(sprites[entity.name],
                                                               (int(entity.width * self.scale),
                                                                int(entity.height * self.scale))),
                                        [self.dx + entity.x, self.dy + entity.y])

            for bullet in bullets:
                # отрисовка пуль
                screen.blit(pygame.transform.scale(sprites['bullet'],
                                                   (int(self.bul_size * self.scale), int(self.bul_size * self.scale))),
                            [self.dx + bullet.x, self.dy + bullet.y])
            if inventory_open:
                # отрисовка инвенторя
                draw_inventory()

    def set_room(self, *rect):
        # получение координат границ текущей комнаты и расчёты координат для её отрисовки
        [self.room_x, self.room_y, self.room_width, self.room_height] = rect
        if self.block_size == 0:
            self.block_size = 35
            print(1)
        self.scale = 35 / self.block_size
        self.x = int(self.block_size * self.scale)
        self.dy = int(- self.room_y * self.block_size + (self.height - self.room_height * self.block_size) / 3)
        self.dx = int(- self.room_x * self.block_size + (self.width - self.room_width * self.block_size) / 2)
        for i in range(self.room_y, self.room_y + self.room_height + 1):
            print(self.map[i][self.room_x: self.room_x + self.room_width + 1])
        print(self.room_x, self.room_y, self.room_width, self.room_height, self.dx, self.dy, self.scale)


class Entity:
    def __init__(self, rect, name):
        [self.x_pos, self.y_pos, self.width_pos, self.height_pos] = rect
        self.name = name

    def get_rect(self):
        return [self.x_pos, self.y_pos, self.width_pos, self.height_pos]

    def move(self, x, y):
        self.x_pos += x
        self.y_pos += y

    def delete(self):
        self.delete()


class Trader(Entity):
    def __init__(self, x, y):
        self.width = int(round(0.7 * window.block_size))
        self.height = int(round(1 * window.block_size))
        self.x = x
        self.y = y
        super().__init__([self.x, self.y + 0.7 * self.height, self.width, 0.3 * self.height], 'trader')

    def get_pos(self):
        return [self.x, self.y]


class Hero(Entity):
    def __init__(self):
        self.room_x, self.room_x1, self.room_y, self.room_y1 = 0, 0, 0, 0
        i, j = 0, 0
        flag = False
        for i in range(window.map_size[1]):
            for j in range(window.map_size[0]):
                if window.map[i][j] == '@':
                    window.map[i][j] = '.'
                    flag = True
                    break
            if flag:
                break
        self.room_init(i, j)
        self.width = int(round(0.7 * window.block_size))
        self.height = int(round(1 * window.block_size))
        self.x = j * window.block_size + window.block_size - self.width // 2
        self.y = i * window.block_size
        super().__init__([self.x, self.y + 0.5 * self.height, self.width, 0.5 * self.height], 'hero')

    def move(self, x, y):
        print(self.x, self.y)
        dx = x
        dy = y
        col = collision(self, dx, dy)
        print(col)
        # перемещение героя
        if col[0] in ['False', 'DoorU', 'DoorD', 'DoorR', 'DoorL']:
            self.x += dx
            self.y += dy
        else:
            dx = 0
            dy = 0
        for i in range(window.map_size[0]):
            tmp = []
            for j in range(window.map_size[1]):
                if j == self.x_pos // window.block_size and i == self.y_pos // window.block_size:
                    tmp.append('@')
                else:
                    tmp.append(window.map[i][j])
            print(tmp)
        # обновление текущей комнаты
        if col[0] == 'DoorD':
            self.room_upd('D')
            print('D')
        elif col[0] == 'DoorU':
            self.room_upd('U')
            print('U')
        elif col[0] == 'DoorR':
            self.room_upd('R')
            print('R')
        elif col[0] == 'DoorL':
            self.room_upd('L')
            print('L')
        super().move(dx, dy)
        # print(dx, dy, self.x // window.block_size, self.y // window.block_size, self.x_pos, self.y_pos)

    def room_init(self, i, j):
        for x in range(j, -1, -1):
            if window.map[i][x] in 'dD0=':
                self.room_x = x
                break
        for y in range(i, -1, -1):
            if window.map[y][j] in 'dD0=':
                self.room_y = y
                break
        for x in range(j, j + 100):
            if window.map[i][x] in 'dD0=':
                self.room_x1 = x
                break
        for y in range(i, i + 100):
            if window.map[y][j] in 'dD0=':
                self.room_y1 = y
                break
        print([self.room_x, self.room_y, self.room_x1 - self.room_x, self.room_y1 - self.room_y])
        window.set_room(self.room_x, self.room_y, self.room_x1 - self.room_x, self.room_y1 - self.room_y)

    def room_upd(self, key):
        if key == 'D':
            self.room_y = self.y // window.block_size
            for x in range(self.x // window.block_size, -1, -1):
                if window.map[self.room_y + 1][x] in 'dD0=':
                    self.room_x = x
                    break
        elif key == 'U':
            for y in range(self.y // window.block_size - 1, -1, -1):
                if window.map[y][self.x // window.block_size] in 'dD0=':
                    self.room_y = y
                    break
            for x in range(self.x // window.block_size, -1, -1):
                if window.map[self.room_y + 1][x] in 'dD0=':
                    self.room_x = x
                    break
        elif key == 'R':
            self.room_x = self.x // window.block_size
            for y in range(self.y // window.block_size, -1, -1):
                if window.map[y][self.room_x + 1] in 'dD0=':
                    self.room_y = y
                    break
        elif key == 'L':
            for x in range(self.x // window.block_size - 1, -1, -1):
                if window.map[self.y // window.block_size][x] in 'dD0=':
                    self.room_x = x
                    break
            for y in range(self.y // window.block_size, -1, -1):
                if window.map[y][self.room_x + 1] in 'dD0=':
                    self.room_y = y
                    break
        for x in range(self.room_x + 1, self.room_x + 100):
            if window.map[self.room_y + 1][x] in 'dD0=':
                self.room_x1 = x
                break
        for y in range(self.room_y + 1, self.room_y + 100):
            if window.map[y][self.room_x + 1] in 'dD0=':
                self.room_y1 = y
                break
        print([self.room_x, self.room_y, self.room_x1 - self.room_x, self.room_y1 - self.room_y])
        if ([window.room_x, window.room_y, window.room_width, window.room_height] !=
                [self.room_x, self.room_y, self.room_x1 - self.room_x, self.room_y1 - self.room_y]):
            if key == 'U':
                self.y -= window.block_size
                super().move(0, -window.block_size)
            elif key == 'D':
                self.y += window.block_size
                super().move(0, window.block_size)
            elif key == 'R':
                self.x += window.block_size
                super().move(window.block_size, 0)
            elif key == 'L':
                self.x -= window.block_size
                super().move(-window.block_size, 0)
        window.set_room(self.room_x, self.room_y, self.room_x1 - self.room_x, self.room_y1 - self.room_y)

    def redraw(self):
        pass

    def get_pos(self):
        return [self.x, self.y]


class Bullet(Window):
    def __init__(self, delt, cords, speed, dmg):
        [self.dx, self.dy] = delt
        self.x, self.y = cords[0], cords[1]
        self.speed = speed
        self.a = True
        self.dmg = dmg

    def get_dmg(self):
        return self.dmg

    def move(self):
        if self.collision():
            self.x += self.speed * self.dx
            self.y += self.speed * self.dy
        else:
            self.a = False

    def get_pos(self):
        return [self.x, self.y]

    def collision(self):
        y1 = int((self.x + self.speed * self.dx) // window.block_size)
        y2 = int((self.x + self.speed * self.dx + window.bul_size) // window.block_size)
        x1 = int((self.y + self.speed * self.dy) // window.block_size)
        x2 = int((self.y + self.speed * self.dy + window.bul_size) // window.block_size)
        if (window.map[x1][y1] not in '#d' and window.map[x2][y1] not in '#d'
                and window.map[x1][y2] not in '#d' and window.map[x2][y2] not in '#d'):
            return True
        return False


class Enemy(Entity):
    def __init__(self, x, y, hp):
        self.hp = hp
        self.speed = 1
        self.width = int(round(0.7 * window.block_size))
        self.height = int(round(1 * window.block_size))
        # print(self.width, self.height, 'Enemy')
        self.x = x
        self.y = y
        super().__init__([self.x, self.y + 0.7 * self.height, self.width, 0.3 * self.height], 'enemy')

    def move(self):
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
        col = collision(self, dx, dy)
        if col[0] == 'hero':
            print(col)
        if col[0] == 'False':
            self.x += dx
            self.y += dy
        else:
            dx = 0
            dy = 0
        super().move(dx, dy)
        if len(col) == 2:
            self.hp -= col[1]
            if col[1] != 0:
                damaged_sound1.play()
        if self.hp < 1:
            enemies.remove(self)
            entities.remove(self)

    def get_pos(self):
        return [self.x, self.y]


class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):
    def __init__(self, b_speed, dmg, magazin, fire_rate, name, ammo, bul_count=1):
        self.b_speed = b_speed
        self.dmg = dmg
        self.magazin = magazin
        self.fire_rate = fire_rate
        self.name = name
        self.ammo = ammo
        self.bul_count = bul_count
        self.cooldown = 0
        super().__init__(self.name)

    def shoot(self, destination):
        print(self.cooldown)
        if self.cooldown == 0:
            self.cooldown = (60 / self.fire_rate) // 1
            print(self.cooldown)
            if self.bul_count % 2 == 1:
                shoot_sound1.play()
                destination[0] -= window.dx
                destination[1] -= window.dy
                cords = [hero.get_pos()[0] + hero.width // 2,
                         hero.get_pos()[1] + hero.height // 2]
                dx = destination[0] - cords[0]
                dy = destination[1] - cords[1]
                if dy != 0:
                    k = math.atan(dx / dy)
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k), -math.cos(k)
                    else:
                        dx, dy = math.sin(k), math.cos(k)
                elif dy == 0:
                    dx, dy = 1, 0
                ammo[inventory[active].ammo] -= 1
                bullets.append(Bullet([dx, dy], cords, self.b_speed, self.dmg))
                if self.bul_count > 1:
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k + math.pi/12), -math.cos(k + math.pi/12)
                    else:
                        dx, dy = math.sin(k + math.pi/12), math.cos(k + math.pi/12)
                    bullets.append(Bullet([dx, dy], cords, self.b_speed, self.dmg))
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k - math.pi/12), -math.cos(k - math.pi/12)
                    else:
                        dx, dy = math.sin(k - math.pi/12), math.cos(k - math.pi/12)
                    bullets.append(Bullet([dx, dy], cords, self.b_speed, self.dmg))

    def cool(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class Staff(Item):
    def __init__(self, name, ammo):
        self.name = name
        self.ammo = ammo


class Chest:
    def __init__(self):
        pass


pygame.init()
a = ''
FPS = 60
guns = [Weapon(2, 25, 25, 3, 'pistol', '9mm'),
        Weapon(3, 40, 30, 5, 'auto', '5.56mm'),
        Weapon(6, 100, 5, 0.7, 'snipe', '7.62mm'),
        Weapon(3, 30, 5, 1, 'shotgun', '12mm', 3)]
ammo = {'9mm': 50, '5.56mm': 60, '7.62mm': 10, '12mm': 10}
active = 0
hp = 100
step = 0
size = width, height = 550, 650
sprites = {'grass': load_image('grass.png'), 'hero': AnimatedSprite(load_image('skin2-gif.png'), 10, 2, 477, 699),
           'box': load_image('box (2).png'), 'trader': load_image('trader.png'),
           'black': load_image('black.jpg'), 'enemy': AnimatedSprite(load_image('skin1-gif.png'), 10, 2, 479, 654),
           'water': load_image('water.png'), 'hp': load_image('hp.png'),
           'bull': load_image('bullet-i.png'), 'open_door': load_image('open_door.png'),
           'closed_door': load_image('closed_door.png'), 'inventory': load_image('inventory1.png'),
           'pistol': load_image('pistol.png'), 'auto': load_image('auto.png'),
           'snipe': load_image('snipe.png'), 'bullet': load_image('bullet.png'),
           'shotgun': load_image('shotgun.png'), 'chest_inventory': load_image('chest_inventory.png'),
           'chest': load_image('chest.png')}
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
shoot_sound1 = pygame.mixer.Sound('sounds/shot_1.wav')
damaged_sound1 = pygame.mixer.Sound('sounds/damaged.wav')
move_sound1 = pygame.mixer.Sound('sounds/move_hero.wav')
bullets = []
bullets_count = guns[active].magazin
enemies = []
traders = []
entities = []
inventory = [guns[0], guns[1], guns[2], guns[3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x, y = 0, 0
grab_from, grab_item = 0, 0
screen = pygame.display.set_mode(size)
window = Window(size)
running = True
menu = True
grab = False
inventory_open = False
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
                        hero = Hero()  # определение героя + # определение комнаты
                        for i in range(window.map_size[1]):
                            for j in range(window.map_size[0]):
                                x = j * window.block_size + window.block_size - hero.width // 2
                                y = i * window.block_size
                                if window.map[i][j] == 'T':
                                    window.map[i][j] = '.'
                                    traders.append(Trader(x, y))
                                elif window.map[i][j] == 'e':
                                    window.map[i][j] = '.'
                                    enemies.append(Enemy(x, y, 100))
                        entities = [hero, *enemies, *traders]
                    else:
                        print('несуществующая карта')
                        terminate()
                elif event.key == pygame.K_BACKSPACE:
                    if len(a) != 0:
                        a = a[:-1]
                else:
                    a += chr(event.key)
        else:
            # управление героем
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_d:
                    move_right = True
                elif event.key == pygame.K_w:
                    move_up = True
                elif event.key == pygame.K_s:
                    move_down = True
                elif event.key == pygame.K_i:
                    inventory_open = not inventory_open
                elif event.key == pygame.K_1:
                    active = 0
                    bullets_count = guns[active].magazin
                elif event.key == pygame.K_2:
                    active = 1
                    bullets_count = guns[active].magazin
                elif event.key == pygame.K_3:
                    active = 2
                    bullets_count = guns[active].magazin
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_w:
                    move_up = False
                elif event.key == pygame.K_s:
                    move_down = False
                elif event.key == pygame.K_u:
                    hp -= 1
                    move_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if inventory_open:
                        # перетаскивание предметов в инвентаре
                        if not grab:
                            x = -1
                            y = -1
                            cords = list(event.pos)
                            if 208 < cords[1] < 245:
                                y = 0
                                dy = 208 - cords[1]
                            else:
                                for i in range(4):
                                    if 10 + 44 * i < cords[1] < 47 + 44 * i:
                                        y = i + 1
                                        dy = 10 + 44 * i - cords[1]
                                        break
                            for i in range(3):
                                if 409 + 47 * i < cords[0] < 446 + 47 * i:
                                    x = i
                                    dx = 409 + 47 * i - cords[0]
                                    break
                            if x != -1 and y != -1:
                                if inventory[y * 3 + x] != 0:
                                    grab = True
                                    grab_from = y * 3 + x
                                    grab_item = inventory[y * 3 + x]
                                    inventory[y * 3 + x] = 0
                                    print('grab {} {}'.format(y, x), grab_item)
                    # стрельба
                    elif type(inventory[active]) is Weapon:
                        if ammo[inventory[active].ammo] > 0:
                            destination = list(event.pos)
                            inventory[active].shoot(destination)
            elif event.type == pygame.MOUSEBUTTONUP:
                # перетаскивание предметов в инвентаре
                if grab:
                    grab = False
                    cords = list(event.pos)
                    x = -1
                    y = -1
                    if 208 < cords[1] < 245:
                        y = 0
                        dy = 208 - cords[1]
                    else:
                        for i in range(4):
                            if 10 + 44 * i < cords[1] < 47 + 44 * i:
                                y = i + 1
                                dy = 10 + 44 * i - cords[1]
                                break
                    for i in range(3):
                        if 409 + 47 * i < cords[0] < 446 + 47 * i:
                            x = i
                            dx = 409 + 47 * i - cords[0]
                            break
                    if x == -1 or y == -1:
                        if x < 400:
                            grab_from = 0
                        else:
                            inventory[grab_from] = grab_item
                            grab_item = 0
                    else:
                        inventory[grab_from], inventory[y * 3 + x] = inventory[y * 3 + x], grab_item
    # движение героя
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
    if hp < 1:
        print('Вы проиграли!')
        terminate()
    for enemy in enemies:
        if (window.room_x + window.room_width > enemy.x // window.block_size > window.room_x - 1 and
                window.room_y + window.room_height > enemy.y // window.block_size > window.room_y - 1):
            enemy.move()
    screen.fill((0, 0, 0))
    for i in range(len(entities)):
        for j in range(len(entities) - 1):
            if entities[j].get_pos()[1] > entities[j + 1].get_pos()[1]:
                entities[j], entities[j + 1] = entities[j + 1], entities[j]
    for weapon in guns:
        weapon.cool()
    if step == 5:
        sprites['hero'].update()
        sprites['enemy'].update()
        step = 0
    else:
        step += 1
    window.render()
    pygame.display.flip()
    clock.tick(FPS)
