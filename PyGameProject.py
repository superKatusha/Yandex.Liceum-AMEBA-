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


def start_screen():
    cords = pygame.mouse.get_pos()
    screen.blit(load_image('fon1.jpg'), (0, 0))
    screen.blit(load_image('TombRaider.png'), (110, 20))
    if 129 < cords[0] < 420:
        if 161 < cords[1] < 228:
            screen.blit(load_image('menu_b1_a.png'), [129, 161])
        elif 298 < cords[1] < 365:
            screen.blit(load_image('menu_b2_a.png'), [129, 298])
        elif 367 < cords[1] < 434:
            screen.blit(load_image('menu_b3_a.png'), [129, 367])
        elif 437 < cords[1] < 504:
            screen.blit(load_image('menu_b4_a.png'), [129, 437])
        elif 506 < cords[1] < 573:
            screen.blit(load_image('menu_b5_a.png'), [129, 506])


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
    screen.blit(pygame.transform.scale(sprites['coin'], (30, 30)), [500, 550])
    screen.blit(load_image('9mm.png'), [500, 350])
    screen.blit(load_image('5.56mm.png'), [500, 400])
    screen.blit(load_image('12mm.png'), [500, 450])
    screen.blit(load_image('7.62mm.png'), [500, 500])
    font = pygame.font.Font(None, 35)
    intro_text = [str(ammo['9mm'])]
    text_coord = [485, 355]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - line_rect[2], text_coord[1]])
    text_coord = [485, 405]
    intro_text = [str(ammo['5.56mm'])]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - line_rect[2], text_coord[1]])
    text_coord = [485, 455]
    intro_text = [str(ammo['12mm'])]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - line_rect[2], text_coord[1]])
    text_coord = [485, 505]
    intro_text = [str(ammo['7.62mm'])]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - line_rect[2], text_coord[1]])
    intro_text = [str(money)]
    text_coord = [485, 555]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0] - line_rect[2], text_coord[1]])
    for i in range(len(inventory)):
        if inventory[i] != 0:
            if i < 3:
                screen.blit(pygame.transform.scale(sprites[inventory[i].name], (37, 37)),
                            [409 + 46 * i, 207])
            else:
                y = 10 + 44 * ((i - 3) // 3)
                x = 409 + 47 * (i % 3)
                screen.blit(pygame.transform.scale(sprites[inventory[i].name], (37, 37)),
                            [x, y])
    if chest_open:
        chest = chests[chest_active]
        screen.blit(sprites['chest_inventory'], [200, 250])
        for i in range(len(chest.inventory)):
            if chest.inventory[i] != 0:
                y = 260 + 44 * (i // 3)
                x = 209 + 47 * (i % 3)
                screen.blit(pygame.transform.scale(sprites[chest.inventory[i].name], (37, 37)),
                            [x, y])
    if grab:
        cords = pygame.mouse.get_pos()
        screen.blit(pygame.transform.scale(sprites[grab_item.name], (37, 37)),
                    [cords[0] + dx, cords[1] + dy])


def save():
    with open('saves/1.txt', 'w') as file:
        tmp = []
        file.write(str(difficulty) + '\n')
        file.write(str(hp) + '\n')
        for elem in ammo:
            tmp.append(elem + ' ' + str(ammo[elem]))
        file.write(' '.join(tmp) + '\n')
        file.write(str(active) + '\n')
        file.write(str(step) + '\n')
        file.write(chest_active + '\n')
        file.write(str(current_level) + '\n')
        file.write(str(window.block_size) + '\n')
        file.write(' '.join([str(window.room_x), str(window.room_y), str(window.room_width), str(window.room_height)]) + '\n')
        file.write(' '.join([str(hero.x), str(hero.y)]) + '\n')
        file.write(str(len(bullets)) + '\n')
        for b in bullets:
            tmp = [str(b.dx), str(b.dy), b.name, str(b.x), str(b.y), str(b.speed), str(b.dmg)]
            file.write(' '.join(tmp) + '\n')
        file.write(str(len(enemies)) + '\n')
        for e in enemies:
            tmp = [str(e.x), str(e.y), e.name, str(e.hp), str(e.fire_rate), str(e.cooldown)]
            file.write(' '.join(tmp) + '\n')
        file.write(str(len(traders)) + '\n')
        for t in traders:
            tmp = [str(t.x), str(t.y)]
            file.write(' '.join(tmp) + '\n')
        file.write(str(len(inventory)) + '\n')
        for i in inventory:
            tmp = ['0']
            if type(i) is Weapon:
                tmp = ['Weapon', str(guns.index(i))]
            elif type(i) is Staff:
                tmp = ['Staff', i.name, str(i.ammo)]
            file.write(' '.join(tmp) + '\n')
        file.write(str(money) + '\n')
        file.write(str(lifes) + '\n')
        file.write(str(points) + '\n')
        file.write(str(level_points))
        default()


def default():
    global a, hp, ammo, active, step, chest_active, bullets, enemies, traders, entities, inventory, x, y, grab_from,\
        grab_item, menu, pause, grab, inventory_open, chest_open, difficulty, money, move_up, move_down, move_right,\
        move_left, trade_denied, settings, trade, death
    difficulty = 1
    hp = 100
    money = 10
    ammo = {'9mm': 50, '5.56mm': 60, '7.62mm': 10, '12mm': 10}
    active = 0
    step = 0
    chest_active = ''
    bullets = []
    enemies = []
    traders = []
    entities = []
    inventory = [guns[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x, y = 0, 0
    grab_from, grab_item = 0, 0
    trade = False
    menu = False
    pause = False
    settings = False
    grab = False
    death = False
    trade_denied = False
    inventory_open = False
    chest_open = False
    move_left, move_right, move_up, move_down = False, False, False, False


def load():
    global a, hp, ammo, active, step, chest_active, bullets, enemies, traders, entities, inventory, x, y, grab_from, \
        grab_item, menu, pause, grab, inventory_open, chest_open, hero, difficulty, money, lifes, points, level_points
    with open('saves/1.txt') as file:
        x = list(map(lambda x: x.strip(), file.readlines()))
        difficulty = float(x[0])
        hp = int(x[1])
        tmp = x[2].split()
        for elem in ammo:
            i = tmp.index(elem)
            ammo[elem] = int(tmp[i + 1])
        active = int(x[3])
        step = int(x[4])
        chest_active = x[5]
        current_level = int(x[6])
        with open(os.path.join('maps', levels[current_level] + '.txt')) as file:
            tmp = file.readlines()
            tmp[0] = tmp[0].lstrip('п»ї')
            window.map_size = list(map(int, tmp[0].split()))
            window.map = list(map(list, tmp[1:]))
            for i in range(window.map_size[1]):
                for j in range(window.map_size[0]):
                    if window.map[i][j] in 'gs@':
                        window.map[i][j] = '.'
        window.block_size = int(x[7])
        [window.room_x, window.room_y, window.room_width, window.room_height] = list(map(int, x[8].split()))
        window.set_room(window.room_x, window.room_y, window.room_width, window.room_height)
        tmp = list(map(int, x[9].split()))
        hero = Hero(tmp[0], tmp[1])
        n = int(x[10])
        cnt = 10
        for i in range(n):
            cnt += 1
            tmp = x[cnt].split()
            bullets.append(Bullet([float(tmp[0]), float(tmp[1])], tmp[2], [float(tmp[3]), float(tmp[4])], int(tmp[5]), int(tmp[6])))
        cnt += 1
        n = int(x[cnt])
        for i in range(n):
            cnt += 1
            tmp = x[cnt].split()
            enemies.append(Enemy(float(tmp[0]), float(tmp[1]), tmp[2], int(tmp[3]), 2))
            enemies[-1].fire_rate = int(tmp[4])
            enemies[-1].cooldown = int(tmp[5])
        cnt += 1
        n = int(x[cnt])
        for i in range(n):
            cnt += 1
            tmp = x[cnt].split()
            traders.append(Trader(int(tmp[0]), int(tmp[1])))
        cnt += 1
        n = int(x[cnt])
        inventory = []
        for i in range(n):
            cnt += 1
            tmp = x[cnt].split()
            if tmp[0] == 'Weapon':
                inventory.append(guns[int(tmp[1])])
            elif tmp[0] == 'Staff':
                inventory.append(Staff(tmp[1], int(tmp[2])))
            else:
                inventory.append(0)
        money = int(x[cnt + 1])
        lifes = int(x[cnt + 2])
        points = int(x[cnt + 3])
        level_points = int(x[cnt + 4])
        entities = [hero, *enemies, *traders]


def draw_pause():
    cords = pygame.mouse.get_pos()
    screen.blit(load_image('dark.png'), [0, 0])
    screen.blit(load_image('pause_continue.png'), [129, 200])
    screen.blit(load_image('pause_restart.png'), [129, 272])
    screen.blit(load_image('pause_save.png'), [129, 344])
    if 129 < cords[0] < 420:
        if 200 < cords[1] < 267:
            screen.blit(load_image('pause_continue_a.png'), [129, 200])
        elif 272 < cords[1] < 339:
            screen.blit(load_image('pause_restart_a.png'), [129, 272])
        elif 344 < cords[1] < 411:
            screen.blit(load_image('pause_save_a.png'), [129, 344])


def draw_settings():
    cords = pygame.mouse.get_pos()
    screen.blit(sprites['fon'], [0, 0])
    k = 0
    if 161 < cords[1] < 228 and 129 < cords[0] < 420:
        k = 1
    if difficulty == 0.8:
        if k == 1:
            screen.blit(load_image('dif_0_a.png'), [129, 161])
        else:
            screen.blit(load_image('dif_0.png'), [129, 161])
    elif difficulty == 1:
        if k == 1:
            screen.blit(load_image('dif_1_a.png'), [129, 161])
        else:
            screen.blit(load_image('dif_1.png'), [129, 161])
    elif difficulty == 1.2:
        if k == 1:
            screen.blit(load_image('dif_2_a.png'), [129, 161])
        else:
            screen.blit(load_image('dif_2.png'), [129, 161])
    elif difficulty == 2:
        if k == 1:
            screen.blit(load_image('dif_3_a.png'), [129, 161])
        else:
            screen.blit(load_image('dif_3.png'), [129, 161])
    if 367 < cords[1] < 434 and 129 < cords[0] < 420:
        screen.blit(load_image('back_to_manu_a.png'), [129, 367])
    else:
        screen.blit(load_image('back_to_manu.png'), [129, 367])


def draw_records():
    screen.blit(sprites['fon'], [0, 0])
    screen.blit(load_image('pergament.png'), [25, 25])
    with open('records/records.txt') as file:
        a = sorted(file.readlines(), key=lambda x: int(x.split()[1]), reverse=True)
    if len(a) > 5:
        a = a[:5]
    font = pygame.font.Font(None, 35)
    intro_text = list(map(lambda x: x.strip(), a))
    text_coord = [100, 100]
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        line_rect = string_rendered.get_rect()
        screen.blit(string_rendered, [text_coord[0], text_coord[1]])
        text_coord[1] += line_rect[3] + 30
    screen.blit(load_image('back_to_manu.png'), [129, 541])
    cords = pygame.mouse.get_pos()
    if 129 < cords[0] < 420:
        if 541 < cords[1] < 608:
            screen.blit(load_image('back_to_manu_a.png'), [129, 541])
    if name_input:
        intro_text = ['Введите имя']
        text_coord = [100, 400]
        for line in intro_text:
            string_rendered = font.render(line, 1, (0, 0, 0))
            line_rect = string_rendered.get_rect()
            screen.blit(string_rendered, [text_coord[0], text_coord[1]])
            text_coord[1] += line_rect[3] + 30
        intro_text = [name + ' ' + str(points)]
        text_coord = [100, 450]
        for line in intro_text:
            string_rendered = font.render(line, 1, (0, 0, 0))
            line_rect = string_rendered.get_rect()
            screen.blit(string_rendered, [text_coord[0], text_coord[1]])
            text_coord[1] += line_rect[3] + 30


def draw_trade(x, y):
    screen.blit(load_image('trader_list.png'), [x, y])
    cords = pygame.mouse.get_pos()
    if x + 10 < cords[0] < x + 190:
        if y + 5 < cords[1] < y + 46:
            screen.blit(load_image('trader_list_1.png'), [x + 10, y + 5])
        elif y + 47 < cords[1] < y + 87:
            screen.blit(load_image('trader_list_2.png'), [x + 10, y + 47])
        elif y + 87 < cords[1] < y + 128:
            screen.blit(load_image('trader_list_3.png'), [x + 10, y + 87])
        elif y + 128 < cords[1] < y + 169:
            screen.blit(load_image('trader_list_4.png'), [x + 10, y + 128])
    if trade_denied:
        screen.blit(load_image('trade_denied.png'), [x - 280, y + 150])


def collision(ent, x, y):
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
                return entity.type
    if (window.map[map_y1][map_x1] in '#=' or
            window.map[map_y1][map_x2] in '#=' or
            window.map[map_y2][map_x1] in '#=' or
            window.map[map_y2][map_x2] in '#='):
        return 'Wall'
    if ent.name == 'hero':
        if (window.map[map_y1][map_x1] == 'd' and
                window.map[map_y1][map_x2] == 'd' and
                window.map[map_y2][map_x1] == '.' and
                window.map[map_y2][map_x2] == '.'):
            return 'DoorD'
        elif (window.map[map_y1][map_x1] == '.' and
                window.map[map_y1][map_x2] == '.' and
                window.map[map_y2][map_x1] == 'd' and
                window.map[map_y2][map_x2] == 'd'):
            return 'DoorU'
        elif (window.map[map_y1][map_x1] == 'd' and
                window.map[map_y1][map_x2] == '.' and
                window.map[map_y2][map_x1] == 'd' and
                window.map[map_y2][map_x2] == '.'):
            return 'DoorR'
        elif (window.map[map_y1][map_x1] == '.' and
                window.map[map_y1][map_x2] == 'd' and
                window.map[map_y2][map_x1] == '.' and
                window.map[map_y2][map_x2] == 'd'):
            return 'DoorL'
    if (window.map[map_y1][map_x1] == 'D' or
            window.map[map_y1][map_x2] == 'D' or
            window.map[map_y2][map_x1] == 'D' or
            window.map[map_y2][map_x2] == 'D'):
        return 'Door'
    return 'False'


def map_init(a):
    global menu, hero, entities
    if os.path.exists(os.path.join('maps', a + '.txt')):
        window.input_map(a + '.txt')
        menu = False
        hero = Hero()  # определение героя + # определение комнаты
        print(window.map_size)
        for i in range(window.map_size[1]):
            for j in range(window.map_size[0]):
                x = j * window.block_size + (window.block_size - hero.width) // 2
                y = i * window.block_size
                if window.map[i][j] == 'T':
                    window.map[i][j] = '.'
                    traders.append(Trader(x, y))
                elif window.map[i][j] == 'g':
                    window.map[i][j] = '.'
                    enemies.append(Enemy(x, y, 'ghost', 100, 2))
                elif window.map[i][j] == 's':
                    window.map[i][j] = '.'
                    enemies.append(Enemy(x, y, 'shooter', 100, 2))
                elif window.map[i][j] == 'B':
                    window.map[i][j] = '.'
                    enemies.append(Enemy(x, y, 'boss', 1000, 1))
        entities = [hero, *enemies, *traders]
        tmp_sprites.append([0, 0, sprites['fon-gif1'], 60])


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
        global chests
        self.map = []
        fullname = os.path.join('maps', name)
        with open(fullname, 'r') as in_file:
            a = in_file.readlines()
            for i in range(len(a)):
                if i == 0:
                    a[0] = a[0].lstrip('п»ї')
                    self.map_size = list(map(int, a[0].split()))
                elif i <= self.map_size[1]:
                    self.map.append(list(a[i].rstrip()))
                else:
                    x = a[i].split()
                    chests[x[0] + ' ' + x[1]] = Chest(x[2])


    def render(self):
        if menu:
            # меню игры
            start_screen()
        elif settings:
            # настройки
            draw_settings()
        elif table_lid:
            # таблица рекордов
            draw_records()
        else:
            indicators()  # отрисовка индикаторов (хп, патроны и т.д.)
            en = []
            # определение врагов в комнате
            for enemy in enemies:
                if (self.room_x + self.room_width > enemy.x // window.block_size > self.room_x - 1 and
                        self.room_y + self.room_height > enemy.y // window.block_size > self.room_y - 1):
                    en.append(enemy)
            # отрисовка карты
            for i in range(self.room_y, self.room_y + self.room_height + 1):
                for j in range(self.room_x, self.room_x + self.room_width + 1):
                    if self.map[i][j] in '.T':
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
                            if trade and entity == traders[trader_active]:
                                draw_trade(self.dx + entity.x + 5, self.dy + entity.y - 190)
            for bullet in bullets:
                # отрисовка пуль
                if bullet.name == 'enemy':
                    b_name = 'bullet_2'
                else:
                    b_name = 'bullet_1'
                screen.blit(pygame.transform.scale(sprites[b_name],
                                                   (int(self.bul_size * self.scale), int(self.bul_size * self.scale))),
                            [self.dx + bullet.x, self.dy + bullet.y])
            if inventory_open:
                # отрисовка инвенторя
                draw_inventory()
            if pause:
                # отрисрвка окна паузы
                draw_pause()
            for sprite in tmp_sprites:
                if type(sprite[2]) is AnimatedSprite:
                    screen.blit(sprite[2].image, [sprite[0], sprite[1]])
                else:
                    screen.blit(sprite[2], [sprite[0], sprite[1]])

    def set_room(self, *rect):
        # получение координат границ текущей комнаты и расчёты координат для её отрисовки
        [self.room_x, self.room_y, self.room_width, self.room_height] = rect
        if self.block_size == 0:
            self.block_size = 35
        self.scale = 35 / self.block_size
        self.x = int(self.block_size * self.scale)
        self.dy = int(- self.room_y * self.block_size + (self.height - self.room_height * self.block_size) / 3)
        self.dx = int(- self.room_x * self.block_size + (self.width - self.room_width * self.block_size) / 2)
        for i in range(self.room_y, self.room_y + self.room_height + 1):
            print(self.map[i][self.room_x: self.room_x + self.room_width + 1])
        print(self.room_x, self.room_y, self.room_width, self.room_height, self.dx, self.dy, self.scale)


class Entity:
    def __init__(self, rect, type):
        [self.x_pos, self.y_pos, self.width_pos, self.height_pos] = rect
        self.type = type

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
        self.name = 'trader'
        super().__init__([self.x, self.y + 0.7 * self.height, self.width, 0.3 * self.height], 'trader')

    def get_pos(self):
        return [self.x, self.y]


class Hero(Entity):
    def __init__(self, *cords):
        self.room_x, self.room_x1, self.room_y, self.room_y1 = 0, 0, 0, 0
        if len(cords) == 0:
            flag = False
            i, j = 0, 0
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
            self.x = j * window.block_size + (window.block_size - self.width) // 2
            self.y = i * window.block_size
        else:
            self.x = cords[0]
            self.y = cords[1]
            self.width = int(round(0.7 * window.block_size))
            self.height = int(round(1 * window.block_size))
        self.name = 'hero'
        super().__init__([self.x, self.y + 0.5 * self.height, self.width, 0.5 * self.height], 'hero')

    def move(self, x, y):
        dx = x
        dy = y
        col = collision(self, dx, dy)
        # перемещение героя
        if col in ['False', 'DoorU', 'DoorD', 'DoorR', 'DoorL']:
            self.x += dx
            self.y += dy
        else:
            dx = 0
            dy = 0
        for i in range(window.map_size[1]):
            tmp = []
            for j in range(window.map_size[0]):
                if j == self.x_pos // window.block_size and i == self.y_pos // window.block_size:
                    tmp.append('@')
                else:
                    tmp.append(window.map[i][j])
        # обновление текущей комнаты
        if col == 'DoorD':
            self.room_upd('D')
            print('D')
        elif col == 'DoorU':
            self.room_upd('U')
            print('U')
        elif col == 'DoorR':
            self.room_upd('R')
            print('R')
        elif col == 'DoorL':
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

    def take_damage(self, damage):
        global hp
        hp -= damage
        if damage > 0:
            damage_sound.play()
        if hp < 0:
            hp = 0

    def get_pos(self):
        return [self.x, self.y]


class Bullet(Window):
    def __init__(self, delt, name, cords, speed, dmg):
        [self.dx, self.dy] = delt
        self.x, self.y = cords[0], cords[1]
        self.speed = speed
        self.name = name
        self.dmg = dmg
        self.side = 7

    def get_dmg(self):
        return self.dmg

    # перемещение пули
    def move(self):
        if self.collision():
            self.x += self.speed * self.dx
            self.y += self.speed * self.dy
        else:
            bullets.remove(self)

    def get_pos(self):
        return [self.x, self.y]

    # проверка на пересечение пули с объектами
    def collision(self):
        y1 = int((self.x + self.speed * self.dx) // window.block_size)
        y2 = int((self.x + self.speed * self.dx + self.side) // window.block_size)
        x1 = int((self.y + self.speed * self.dy) // window.block_size)
        x2 = int((self.y + self.speed * self.dy + self.side) // window.block_size)
        if (window.map[x1][y1] in '#Dd' or window.map[x2][y1] in '#Dd'
                or window.map[x1][y2] in '#Dd' or window.map[x2][y2] in '#Dd'):
            return False
        for entity in entities:
            x1, y1, width, height = entity.x, entity.y, entity.width, entity.height
            x2 = x1 + width
            y2 = y1 + height
            if (entity.type == 'hero' and self.name == 'enemy') or (entity.type == 'enemy' and self.name == 'hero'):
                if ((x2 >= self.x >= x1 and y2 >= self.y >= y1) or
                        (x2 >= self.x >= x1 and y2 >= self.y + self.side >= y1) or
                        (x2 >= self.x + self.side >= x1 and y2 >= self.y >= y1) or
                        (x2 >= self.x + self.side >= x1 and y2 >= self.y + self.side >= y1)):
                    entity.take_damage(self.dmg)
                    return False
        return True


class Enemy(Entity):
    def __init__(self, x, y, name, hp, fire_rate):
        self.hp = hp
        self.speed = 1
        if difficulty == 2:
            self.speed = 1.5
        self.fire_rate = int(60 / fire_rate)
        self.cooldown = self.fire_rate
        self.width = int(round(0.7 * window.block_size))
        self.height = int(round(1 * window.block_size))
        self.dmg = int(15 * difficulty)
        self.b_speed = 2
        self.name = name
        self.type = 'enemy'
        self.col = 'False'
        self.step = 0
        # print(self.width, self.height, 'Enemy')
        self.x = x
        self.y = y
        super().__init__([self.x, self.y + 0.7 * self.height, self.width, 0.3 * self.height], self.type)

    # перемещение врагов
    def move(self):
        if self.name in ['ghost', 'boss']:
            destination = hero.get_pos()
            dx = destination[0] - self.x
            dy = destination[1] - self.y
            if dy != 0 and dx != 0:
                k = math.atan(dx / dy)
                if destination[1] - self.y < 0:
                    dx, dy = -math.sin(k) * self.speed, -math.cos(k) * self.speed
                else:
                    dx, dy = math.sin(k), math.cos(k)
            elif dx == 0 and dy > 0:
                dx, dy = 0, self.speed
            elif dy == 0 and dx > 0:
                dx, dy = self.speed, 0
            self.col = 'False'
            if self.name == 'ghost':
                col = collision(self, dx, 0)
                if col not in ['False', 'Wall']:
                    dx = 0
                col1 = collision(self, 0, dy)
                if col1 not in ['False', 'Wall']:
                    dy = 0
            else:
                col = collision(self, dx, 0)
                if col not in ['False']:
                    dx = 0
                col1 = collision(self, 0, dy)
                if col1 not in ['False']:
                    dy = 0
            if dx == 0 and dy != 0:
                dy = int(dy / abs(dy) * self.speed)
            elif dx != 0 and dy == 0:
                dx = int(dx / abs(dx) * self.speed)
            self.x += dx
            self.y += dy
            super().move(dx, dy)
            if 'hero' in [col, col1]:
                self.col = 'hero'

    # атака врагов
    def atack(self):
        global hp
        if self.cooldown == 0:
            self.cooldown = self.fire_rate
            if self.name == 'ghost':
                if self.col == 'hero':
                    hp -= 15
                    if hp < 0:
                        hp = 0
            elif self.name == 'shooter':
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
                else:
                    dx, dy = 1, 0
                bullets.append(Bullet([dx, dy], 'enemy', [self.x + 0.5 * window.block_size,
                                                          self.y + 0.5 * window.block_size], self.b_speed, self.dmg))
            elif self.name == 'boss':
                print(self.step)
                if self.step < 6:
                    self.cooldown = 0
                if self.step == 1 or self.step == 6:
                    destination = [hero.x_pos, hero.y_pos]
                    cords = [self.x + 0.5 * window.block_size, self.y + 0.5 * window.block_size]
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
                    bullets.append(Bullet([dx, dy], 'enemy', cords, self.b_speed, self.dmg))
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k + math.pi / 12), -math.cos(k + math.pi / 12)
                    else:
                        dx, dy = math.sin(k + math.pi / 12), math.cos(k + math.pi / 12)
                    bullets.append(Bullet([dx, dy], 'enemy', cords, self.b_speed, self.dmg))
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k - math.pi / 12), -math.cos(k - math.pi / 12)
                    else:
                        dx, dy = math.sin(k - math.pi / 12), math.cos(k - math.pi / 12)
                    bullets.append(Bullet([dx, dy], 'enemy', cords, self.b_speed, self.dmg))
                elif self.step == 7:
                    destination = [hero.x_pos, hero.y_pos]
                    cords = [self.x + 0.5 * window.block_size, self.y + 0.5 * window.block_size]
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
                    for i in range(24):
                        if destination[1] - cords[1] < 0:
                            dx, dy = -math.sin(k + i * math.pi / 12), -math.cos(k + i * math.pi / 12)
                        else:
                            dx, dy = math.sin(k + i * math.pi / 12), math.cos(k + i * math.pi / 12)
                        bullets.append(Bullet([dx, dy], 'enemy', cords, self.b_speed, self.dmg))
                    self.step = 0
                self.step += 1

    # задержка атаки
    def cool(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    # получение урона
    def take_damage(self, damage):
        global money, victory, step, level_points
        self.hp -= damage
        if damage != 0:
            damaged_sound1.play()
        if self.hp < 1:
            if self.name == 'boss':
                level_points += 1000
                victory = True
                step = -1
            else:
                level_points += 200
            money += 1
            tmp_sprites.append([window.dx + self.x, self.y_pos - window.block_size + window.dy,
                                AnimatedSprite(load_image('coin-gif.png'), 10, 6, 20, 20), 60])
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
        self.dmg = int(dmg / difficulty)
        self.magazin = magazin
        self.fire_rate = fire_rate
        self.name = name
        self.ammo = ammo
        self.bul_count = bul_count
        self.cooldown = 0
        super().__init__(self.name)

    def shoot(self, destination):
        if self.cooldown == 0:
            self.cooldown = (60 / self.fire_rate) // 1
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
                bullets.append(Bullet([dx, dy], 'hero', cords, self.b_speed, self.dmg))
                if self.bul_count > 1:
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k + math.pi/12), -math.cos(k + math.pi/12)
                    else:
                        dx, dy = math.sin(k + math.pi/12), math.cos(k + math.pi/12)
                    bullets.append(Bullet([dx, dy], 'hero', cords, self.b_speed, self.dmg))
                    if destination[1] - cords[1] < 0:
                        dx, dy = -math.sin(k - math.pi/12), -math.cos(k - math.pi/12)
                    else:
                        dx, dy = math.sin(k - math.pi/12), math.cos(k - math.pi/12)
                    bullets.append(Bullet([dx, dy], 'hero', cords, self.b_speed, self.dmg))

    def cool(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class Staff(Item):
    def __init__(self, name, ammo):
        self.name = name
        self.ammo = ammo


class Chest:
    def __init__(self, type):
        self.type = type
        self.inventory = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.fill()

    def fill(self):
        for i in range(len(self.inventory)):
            luck = random.randint(1, 100)
            prs = 0
            for loot in chest_types[self.type]:
                if luck <= loot[1] + prs:
                    self.inventory[i] = loot[0]
                    break
                prs += loot[1]


pygame.init()
a = ''
FPS = 60
hp = 100
difficulty = 1
money = 10
guns = [Weapon(2, 25, 25, 3, 'pistol', '9mm'),
        Weapon(3, 40, 30, 5, 'auto', '5.56mm'),
        Weapon(6, 100, 5, 0.7, 'snipe', '7.62mm'),
        Weapon(3, 40, 5, 1, 'shotgun', '12mm', 3)]
ammo = {'9mm': 50, '5.56mm': 60, '7.62mm': 10, '12mm': 10}
chests = {}
lifes = 3
active = 0
step = 0
points = 0
level_points = 0
size = width, height = 550, 650
sprites = {'grass': load_image('grass.png'), 'hero': AnimatedSprite(load_image('skin2-gif.png'), 10, 2, 477, 699),
           'box': load_image('box (2).png'), 'trader': load_image('trader.png'),
           'black': load_image('black.jpg'), 'ghost': AnimatedSprite(load_image('skin1-gif.png'), 10, 2, 479, 654),
           'hp': load_image('hp.png'), 'boss': load_image('boss.png'),
           'bull': load_image('bullet-i.png'), 'open_door': load_image('open_door.png'),
           'closed_door': load_image('closed_door.png'), 'inventory': load_image('inventory1.png'),
           'pistol': load_image('pistol.png'), 'auto': load_image('auto.png'), 'coin': load_image('coin.png'),
           'snipe': load_image('snipe.png'), 'bullet_1': load_image('bullet.png'),
           'bullet_2': load_image('bullet (1).png'), 'fon': load_image('fon.png'),
           'shotgun': load_image('shotgun.png'), 'chest_inventory': load_image('chest_inventory.png'),
           'chest': load_image('chest.png'), 'shooter': load_image('shooting.png'),
           'fon-gif': AnimatedSprite(load_image('fon-gif.png'), 10, 6, 550, 650),
           'fon-gif1': AnimatedSprite(load_image('fon-gif(1).png'), 10, 6, 550, 650),
           }
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
shoot_sound1 = pygame.mixer.Sound('sounds/shot_1.wav')
damaged_sound1 = pygame.mixer.Sound('sounds/damaged.wav')
damage_sound = pygame.mixer.Sound('sounds/damage.wav')
move_sound1 = pygame.mixer.Sound('sounds/move_hero1.wav')
cash = pygame.mixer.Sound('sounds/purchase.wav')
death_sound = pygame.mixer.Sound('sounds/death.wav')
chest_types = {'starter': [[guns[0], 25], [guns[1], 10], [guns[2], 2], [guns[3], 1]]}
chest_active = ''
name = ''
trader_active = 0
levels = ['arena', 'levelbykvadron']
current_level = 0
tmp_sprites = []
bullets = []
enemies = []
traders = []
entities = []
inventory = [guns[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x, y = 0, 0
grab_from, grab_item = 0, 0
screen = pygame.display.set_mode(size)
window = Window(size)
running = True
trade = False
menu = True
victory = False
death = False
pause = False
table_lid = False
settings = False
grab = False
name_input = False
trade_denied = False
inventory_open = False
chest_open = False
move_left, move_right, move_up, move_down = False, False, False, False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = list(event.pos)
                a = levels[current_level]
                if 129 < cords[0] < 420:
                    if 161 < cords[1] < 228:
                        map_init(a)
                    elif 298 < cords[1] < 365:
                        menu = False
                        load()
                    elif 367 < cords[1] < 434:
                        menu = False
                        table_lid = True
                    elif 437 < cords[1] < 504:
                        menu = False
                        settings = True
                    elif 506 < cords[1] < 573:
                        terminate()
        elif settings:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = list(event.pos)
                if 129 < cords[0] < 420:
                    if 161 < cords[1] < 228:
                        if difficulty == 1.2:
                            difficulty = 2
                        elif difficulty == 2:
                            difficulty = 0.8
                        else:
                            difficulty += 0.2
                    elif 367 < cords[1] < 434:
                        settings = False
                        menu = True
        elif pause:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = list(event.pos)
                if 129 < cords[0] < 420:
                    if 200 < cords[1] < 267:
                        pause = False
                    elif 272 < cords[1] < 339:
                        lifes -= 1
                        death = True
                        pause = False
                        death_sound.play()
                        step = 0
                    elif 344 < cords[1] < 411:
                        save()
                        pause = False
                        menu = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
        elif table_lid:
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    with open('records/records.txt') as file:
                        x = list(map(lambda x: x.split(), file.readlines()))
                    for elem in x:
                        elem[1] = int(elem[1])
                    x.append([name, points])
                    x = sorted(x, key=lambda player: player[1], reverse=True)
                    with open('records/records.txt', 'w') as file:
                        for elem in x:
                            file.write(elem[0] + ' ' + str(elem[1]) + '\n')
                    points = 0
                    name = ''
                    name_input = False
                elif event.key == pygame.K_BACKSPACE:
                    if len(name) != 0:
                        name = name[:-1]
                else:
                    name += chr(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cords = list(event.pos)
                if 129 < cords[0] < 420:
                    if 541 < cords[1] < 608:
                        table_lid = False
                        menu = True
        else:
            # управление героем
            if event.type == pygame.KEYDOWN:
                if not inventory_open:
                    if event.key == pygame.K_a:
                        move_left = True
                    elif event.key == pygame.K_d:
                        move_right = True
                    elif event.key == pygame.K_w:
                        move_up = True
                    elif event.key == pygame.K_s:
                        move_down = True
                if event.key == pygame.K_i:
                    inventory_open = not inventory_open
                    chest_open = False
                    move_left, move_right, move_up, move_down = False, False, False, False
                elif event.key == pygame.K_1:
                    active = 0
                    if type(inventory[active]) is Weapon:
                        bullets_count = ammo[inventory[active].ammo]
                    else:
                        bullets_count = -1
                elif event.key == pygame.K_2:
                    active = 1
                    if type(inventory[active]) is Weapon:
                        bullets_count = ammo[inventory[active].ammo]
                    else:
                        bullets_count = -1
                elif event.key == pygame.K_3:
                    active = 2
                    if type(inventory[active]) is Weapon:
                        bullets_count = ammo[inventory[active].ammo]
                    else:
                        bullets_count = -1
                elif event.key == pygame.K_ESCAPE:
                    pause = True
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
                    cords = list(event.pos)
                    map_x = (cords[0] - window.dx) // window.block_size
                    map_y = (cords[1] - window.dy) // window.block_size
                    if not trade:
                        # детект нажатия на торговца
                        trader_active = -1
                        for i in range(len(traders)):
                            if (traders[i].x + window.dx < cords[0] < traders[i].x + traders[i].width + window.dx and
                                    traders[i].y + window.dy < cords[1] < traders[i].y + traders[i].height + window.dy):
                                trader_active = i
                                break
                    if inventory_open:
                        # перетаскивание предметов в инвентаре
                        if not grab:
                            x = -1
                            y = -1
                            ch = 0
                            if cords[1] < 245:
                                if 208 < cords[1] < 245:
                                    y = 0
                                    dy = 208 - cords[1]
                                else:
                                    for i in range(4):
                                        if 10 + 44 * i < cords[1] < 47 + 44 * i:
                                            y = i + 1
                                            dy = 10 + 44 * i - cords[1]
                                            break
                            else:
                                ch = 1
                                for i in range(3):
                                    if 260 + 44 * i < cords[1] < 297 + 44 * i:
                                        y = i
                                        dy = 260 + 44 * i - cords[1]
                                        break
                            if cords[0] > 400:
                                for i in range(3):
                                    if 409 + 47 * i < cords[0] < 446 + 47 * i:
                                        x = i
                                        dx = 409 + 47 * i - cords[0]
                                        break
                            else:
                                ch = 1
                                for i in range(3):
                                    if 209 + 47 * i < cords[0] < 246 + 47 * i:
                                        x = i
                                        dx = 209 + 47 * i - cords[0]
                                        break
                            if x != -1 and y != -1:
                                if ch == 0:
                                    if inventory[y * 3 + x] != 0:
                                        grab = True
                                        grab_from = [y * 3 + x, 'in']
                                        grab_item = inventory[y * 3 + x]
                                        inventory[y * 3 + x] = 0
                                        print('grab {} {}'.format(y, x), grab_item)
                                else:
                                    chest = chests[chest_active]
                                    if chest.inventory[y * 3 + x] != 0:
                                        grab = True
                                        grab_from = [y * 3 + x, 'ch']
                                        grab_item = chest.inventory[y * 3 + x]
                                        chest.inventory[y * 3 + x] = 0
                                        print('grab {} {}'.format(y, x), grab_item)
                    elif trade:
                        x = window.dx + traders[trader_active].x + traders[trader_active].width + 5
                        y = window.dy + traders[trader_active].y - 190
                        if x + 10 < cords[0] < x + 190:
                            if y + 5 < cords[1] < y + 46:
                                if money >= 5:
                                    money -= 5
                                    ammo['9mm'] += 35
                                    cash.play()
                                else:
                                    trade_denied = True
                            elif y + 47 < cords[1] < y + 87:
                                if money >= 5:
                                    money -= 5
                                    ammo['5.56mm'] += 25
                                    cash.play()
                                else:
                                    trade_denied = True
                            elif y + 87 < cords[1] < y + 128:
                                if money >= 5:
                                    money -= 5
                                    ammo['12mm'] += 15
                                    cash.play()
                                else:
                                    trade_denied = True
                            elif y + 128 < cords[1] < y + 169:
                                if money >= 5:
                                    money -= 5
                                    ammo['7.62mm'] += 10
                                    cash.play()
                                else:
                                    trade_denied = True
                    # взаимодействие с сундуком
                    elif window.map[map_y][map_x] == 'c':
                        if (abs(hero.x // window.block_size - map_x) < 3 and
                                abs(hero.y // window.block_size - map_y) < 3):
                            inventory_open = True
                            chest_open = True
                            chest_active = '{} {}'.format(map_x, map_y)
                    elif trader_active != -1:
                        if (abs(hero.x - traders[trader_active].x) <= window.block_size and
                                abs(hero.y - traders[trader_active].y) <= window.block_size):
                            trade = True
                    # стрельба
                    elif type(inventory[active]) is Weapon:
                        if ammo[inventory[active].ammo] > 0:
                            inventory[active].shoot(cords)
            elif event.type == pygame.MOUSEBUTTONUP:
                # перетаскивание предметов в инвентаре
                if grab:
                    grab = False
                    cords = list(event.pos)
                    x = -1
                    y = -1
                    ch = 0
                    if cords[1] < 245:
                        if 208 < cords[1] < 245:
                            y = 0
                            dy = 208 - cords[1]
                        else:
                            for i in range(4):
                                if 10 + 44 * i < cords[1] < 47 + 44 * i:
                                    y = i + 1
                                    dy = 10 + 44 * i - cords[1]
                                    break
                    else:
                        ch = 1
                        for i in range(3):
                            if 260 + 44 * i < cords[1] < 297 + 44 * i:
                                y = i
                                dy = 260 + 44 * i - cords[1]
                                break
                    if cords[0] > 400:
                        for i in range(3):
                            if 409 + 47 * i < cords[0] < 446 + 47 * i:
                                x = i
                                dx = 409 + 47 * i - cords[0]
                                break
                    else:
                        ch = 1
                        for i in range(3):
                            if 209 + 47 * i < cords[0] < 246 + 47 * i:
                                x = i
                                dx = 209 + 47 * i - cords[0]
                                break
                    if x == -1 or y == -1:
                        if 350 > x > 200 and 400 > y > 250 or x > 400:
                            if grab_from[1] == 'in':
                                inventory[grab_from[0]] = grab_item
                            else:
                                chests[chest_active].inventory[grab_from[0]] = grab_item
                            grab_item = 0
                        else:
                            grab_from = 0
                    else:
                        if grab_from[1] == 'in' and ch == 0:
                            inventory[grab_from[0]], inventory[y * 3 + x] = inventory[y * 3 + x], grab_item
                        elif grab_from[1] == 'in' and ch == 1:
                            inventory[grab_from[0]], chests[chest_active].inventory[y * 3 + x] = \
                                chests[chest_active].inventory[y * 3 + x], grab_item
                        elif grab_from[1] == 'ch' and ch == 0:
                            chests[chest_active].inventory[grab_from[0]], inventory[y * 3 + x] = inventory[
                                                                                        y * 3 + x], grab_item
                        elif grab_from[1] == 'ch' and ch == 1:
                            chests[chest_active].inventory[grab_from[0]], chests[chest_active].inventory[y * 3 + x] = \
                                chests[chest_active].inventory[y * 3 + x], grab_item
    if not pause and not death and not victory:
        if move_left or move_right or move_down or move_up:
            trade = False
            trade_denied = False
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
        if hp < 1:
            lifes -= 1
            death = True
            death_sound.play()
            step = -1
        for enemy in enemies:
            if (window.room_x + window.room_width > enemy.x // window.block_size > window.room_x - 1 and
                    window.room_y + window.room_height > enemy.y // window.block_size > window.room_y - 1):
                enemy.move()
                enemy.atack()
                enemy.cool()
        screen.fill((0, 0, 0))
        for i in range(len(entities)):
            for j in range(len(entities) - 1):
                if entities[j].get_pos()[1] > entities[j + 1].get_pos()[1]:
                    entities[j], entities[j + 1] = entities[j + 1], entities[j]
        for weapon in guns:
            weapon.cool()
        for sprite in tmp_sprites:
            if type(sprite[2]) is AnimatedSprite:
                sprite[2].update()
            sprite[3] -= 1
            if sprite[3] == 0:
                tmp_sprites.remove(sprite)
        if step == 5:
            sprites['hero'].update()
            sprites['ghost'].update()
            step = 0
        else:
            step += 1
    if death:
        step += 1
        if step == 1:
            tmp_sprites.append([0, 0, sprites['fon-gif'], 60])
        if step == 60:
            tmp_sprites.append([0, 0, load_image('black.jpg'), 180])
            if lifes == 2:
                tmp_sprites.append([125, 225, load_image('2lifes.png'), 178])
            elif lifes == 1:
                tmp_sprites.append([125, 225, load_image('1lifes.png'), 178])
            else:
                tmp_sprites.append([125, 225, load_image('0lifes.png'), 178])
            tmp_sprites.append([0, 0, sprites['fon-gif1'], 60])
        if step == 179:
            tmp_sprites.append([0, 0, sprites['fon-gif'], 60])
        for sprite in tmp_sprites:
            if type(sprite[2]) is AnimatedSprite:
                sprite[2].update()
            sprite[3] -= 1
            if sprite[3] == 0:
                tmp_sprites.remove(sprite)
        if len(tmp_sprites) == 0:
            default()
            if lifes != 0:
                map_init(a)
            else:
                menu = True
                lifes = 3
                current_level = 0
                points = 0
    if victory:
        step += 1
        if step == 1:
            tmp_sprites.append([0, 0, sprites['fon-gif'], 59])
        if step == 60:
            tmp_sprites.append([0, 0, load_image('black.jpg'), 180])
            if lifes == 3:
                tmp_sprites.append([125, 225, load_image('3lifes.png'), 178])
            elif lifes == 2:
                tmp_sprites.append([125, 225, load_image('2lifes.png'), 178])
            elif lifes == 1:
                tmp_sprites.append([125, 225, load_image('1lifes.png'), 178])
            else:
                tmp_sprites.append([125, 225, load_image('0lifes.png'), 178])
            tmp_sprites.append([0, 0, sprites['fon-gif1'], 60])
        if step == 179:
            tmp_sprites.append([0, 0, sprites['fon-gif'], 60])
        for sprite in tmp_sprites:
            if type(sprite[2]) is AnimatedSprite:
                sprite[2].update()
            sprite[3] -= 1
            if sprite[3] == 0:
                tmp_sprites.remove(sprite)
        if len(tmp_sprites) == 0:
            points += level_points
            default()
            victory = False
            if current_level == 1:
                current_level = 0
                table_lid = True
                name_input = True
            else:
                current_level += 1
                map_init(levels[current_level])
    window.render()
    pygame.display.flip()
    clock.tick(FPS)
