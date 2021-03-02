import pygame
from pygame import *
import os
from Entities import Player
from Entities import Bullet
from Enemies import Enemy, EnemyBullet
import Menu
import pyautogui
import random
import pyganim

# WIN_WIDTH, WIN_HEIGHT = 700, 700
# WIN_WIDTH, WIN_HEIGHT = 1920, 1080
WIN_WIDTH, WIN_HEIGHT = pyautogui.size()[0], pyautogui.size()[1]

size = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

pygame.init()  # Инициация PyGame, обязательная строчка
screen = pygame.display.set_mode(size, pygame.SRCALPHA)  # Создаем окошко
screen.fill((0, 0, 0, 0))


def load_image(name, colorkey=None):
    fullname = os.path.join('data/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, WIN_WIDTH, WIN_HEIGHT)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, group2):
        super().__init__(group, group2)
        self.rect = None


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(PLATFORM_WIDTH * pos_x, PLATFORM_HEIGHT * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Portal(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(entity_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(PLATFORM_WIDTH * pos_x, PLATFORM_HEIGHT * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Beer(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(entity_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(PLATFORM_WIDTH * pos_x, PLATFORM_HEIGHT * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


tiles_group = SpriteGroup()
all_sprites = SpriteGroup()
entity_group = SpriteGroup()
enemy_group = SpriteGroup()
bullets_group = SpriteGroup()
portals = SpriteGroup()
beer_group = SpriteGroup()


def generate_level(level):
    x = 0
    y = 0
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'p':
                portal = Portal('portal', x, y)
                portals.add(portal)
            elif level[y][x] == 'b':
                beer = Beer('beer', x, y)
                beer_group.add(beer)
                all_sprites.add(beer)
            elif level[y][x] == '@':
                new_player = Player(PLATFORM_WIDTH * x + PLATFORM_WIDTH // 2, PLATFORM_HEIGHT * y, all_sprites)
                ll = list(level[y])
                ll[x] = '.'
                level[y] = ll
                all_sprites.add(new_player)
            elif level[y][x] == 'e':
                new_enemy = Enemy(PLATFORM_WIDTH * x, PLATFORM_HEIGHT * y, random.randrange(2, 5), bullets_group, all_sprites, None)
                enemy_group.add(new_enemy)
                entity_group.add(new_enemy)

    for en in enemy_group:
        en.hero = new_player

    # вернем игрока, а также размер поля в клетках
    return new_player, enemy_group, x, y


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    # l = min(0, l)  # Не движемся дальше левой границы
    # l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    # t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    # t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


# Объявляем переменные
FPS = 60

PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 80
PLATFORM_COLOR = "black"
BACKGROUND_COLOR = "white"
extra_speed = 0
count = 0

tile_images = {
    'wall': load_image('textures/main/walls/metal3.png'),
    'portal': load_image('textures/objects/portal.png'),
    'beer': load_image('textures/objects/beer.png')
}

levels = {
    '1': load_level('map.map'),
    '2': load_level('map2.map')
}
bg_menu = load_image('main_menu/scr_for_menu.jpg')


def main():
    global left, right, up, hero, enemy, screenshot, PLAY_MENU_MUS, extra_speed, count

    level = 1

    pygame.display.set_caption("test")

    running, pause, menu, process = 1, 2, 0, True
    state = menu

    hero, enemy_group, max_x, max_y = generate_level(levels[str(level)])
    entity_group.add(hero)
    for spr in enemy_group:
        entity_group.add(spr)

    total_level_width = (max_x + 1) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = (max_y + 1) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    clock = pygame.time.Clock()
    left = False
    right = False
    up = False
    extra_speed = 0
    start = None

    camera.update(hero)

    screen2 = Surface(size, pygame.SRCALPHA)

    PLAY_MENU_MUS = False

    while process:  # Основной цикл программы
        if state == running:
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    process = False

                if event.type == KEYDOWN and event.key == K_a:
                    left = True
                if event.type == KEYUP and event.key == K_a:
                    left = False

                if event.type == KEYDOWN and event.key == K_d:
                    right = True
                if event.type == KEYUP and event.key == K_d:
                    right = False

                if event.type == KEYDOWN and (event.key == K_w or event.key == K_SPACE):
                    up = True
                if event.type == KEYUP and (event.key == K_w or event.key == K_SPACE):
                    up = False

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    state = pause
                    up = False
                    left = False
                    right = False
                    back = screen.subsurface(screen.get_rect())
                    screenshot = Surface(size)
                    screenshot.blit(back, (0, 0))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        hero.shoot(bullets_group, all_sprites, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            screen.fill('black')
            # oejfosfp nbgjhgytyfd6

            camera.update(hero)

            for spr in all_sprites:
                screen.blit(spr.image, camera.apply(spr))
            for e in entity_group:
                screen.blit(e.image, camera.apply(e))
            for bul in bullets_group:
                screen.blit(bul.image, camera.apply(bul))
                if isinstance(bul, EnemyBullet):
                    bul.update_bullet(tiles_group)
                elif isinstance(bul, Bullet):
                    bul.update_bullet(tiles_group, enemy_group)

            if sprite.spritecollide(hero, portals, False):
                for i in all_sprites:
                    i.kill()
                level += 1
                hero, enemy_group, max_x, max_y = generate_level(levels[str(level)])

            for b in beer_group:
                if sprite.collide_rect(hero, b):
                    extra_speed = 8
                    start = pygame.time.get_ticks()
                    b.kill()
            hits = sprite.spritecollide(hero, enemy_group, False)
            if hits:
                process = False

            if extra_speed > 0:
                if pygame.time.get_ticks() - start > 5000:
                    extra_speed = 0

            hero.update(left, right, up, tiles_group, screen, extra_speed)

            for e in enemy_group:
                e.update(tiles_group)

            # print(len(all_sprites))

        elif state == pause:
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    process = False

                if event.type == MOUSEBUTTONDOWN and 30 < event.pos[0] < 280 and \
                        30 < event.pos[1] < 80:
                    state = menu
                if event.type == MOUSEBUTTONDOWN and 280 < event.pos[0] < 480 and \
                        30 < event.pos[1] < 80:
                    state = running

            screen.blit(screenshot, (0, 0))
            Menu.menu_pause(screen2, screenshot)

            screen.blit(screen2, (0, 0))
            screen2.fill((0, 0, 0, 0))

        elif state == menu:
            if PLAY_MENU_MUS is False:
                pygame.mixer.music.load('data/music/main_menu_cur.mp3')
                pygame.mixer.music.set_volume(0.15)
                pygame.mixer.music.play(-1)
                PLAY_MENU_MUS = True

            screen.fill('black')
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    process = False

                if event.type == MOUSEBUTTONDOWN and 200 < event.pos[0] < 500 and \
                        400 < event.pos[1] < 450:

                    for i in all_sprites:
                        i.kill()
                    hero.kill()
                    level = 1
                    hero, enemy_group, max_x, max_y = generate_level(load_level('map.map'))

                    state = running
                    pygame.mixer.music.stop()
                    PLAY_MENU_MUS = False

                if event.type == MOUSEBUTTONDOWN and 200 < event.pos[0] < 500 and \
                        520 < event.pos[1] < 570:
                    process = False

            Menu.main_menu(screen, bg_menu)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
