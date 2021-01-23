import pygame
from pygame import *
from Entities import Bullet
import math
import time

# WIN_WIDTH, WIN_HEIGHT = 1920, 1080
WIN_WIDTH, WIN_HEIGHT = 700, 700

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

ENEMY_MOVE_SPEED = 6
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 70

COLOR = 'red'

BULLET_SIZE = 10
BULLET_SPEED = 15


class EnemyBullet(Bullet):
    def __init__(self, x, y, speedx, speedy):
        super().__init__(x, y, speedx, speedy)


def find_enemy_speed(pos_mouse_x, pos_mouse_y, self_pos_x, self_pos_y):

    x = self_pos_x
    y = self_pos_y

    angel = math.radians(abs(math.degrees(math.atan2(abs(pos_mouse_x - x), abs(y - pos_mouse_y))) - 90))

    print(f"hero x: {x} y: {y}")
    print(f'angel: {math.degrees(angel)} degrees')
    print(f"mouse: x: {pos_mouse_x} y: {pos_mouse_y}")
    print()

    speed_x, speed_y = 0, 0

    if x < pos_mouse_x and y > pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = -(math.sin(angel)) * BULLET_SPEED
    elif x > pos_mouse_x and y > pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = -(math.sin(angel) * BULLET_SPEED)
    elif x > pos_mouse_x and y < pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x < pos_mouse_x and y < pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x == pos_mouse_x:
        speed_x = 0
        if y > pos_mouse_y:
            speed_y = -BULLET_SPEED
        elif y < pos_mouse_y:
            speed_y = BULLET_SPEED
        else:
            speed_y = BULLET_SPEED
    elif y == pos_mouse_y:
        speed_y = 0
        if x > pos_mouse_x:
            speed_x = -BULLET_SPEED
        elif x < pos_mouse_x:
            speed_x = BULLET_SPEED
        else:
            speed_x = 0
            speed_y = BULLET_SPEED

    return speed_x, speed_y


class Enemy(sprite.Sprite):
    def __init__(self, x, y, bullet_group, all_sprites, hero):
        sprite.Sprite.__init__(self)

        self.onGround = False  # На земле ли я?

        self.yvel = 0  # скорость вертикального перемещения
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.image = Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.pos = (self.rect.x, self.rect.y)

        self.bullets_group = bullet_group
        self.all_sprites = all_sprites

        self.hero = hero

        self.bullet_speed = 1

        self.shoot_pass = True

        self.start_timer = 0

        self.left = False
        self.right = False
        self.up = False

    def update(self, platforms):

        self.II(self.hero.rect.centerx, self.hero.rect.centery, platforms, self.hero)

        if self.left:
            self.xvel = -ENEMY_MOVE_SPEED  # Лево = x- n

        if self.right:
            self.xvel = ENEMY_MOVE_SPEED  # Право = x + n

        if not (self.left or self.right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if self.up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def II(self, hero_pos_x, hero_pos_y, platforms, hero):
        r = 500
        if (hero.rect.centerx - self.rect.centerx) ** 2 + (hero.rect.centery - self.rect.centery) ** 2 <= r * r:
            print()
            if pygame.time.get_ticks() - self.start_timer > 300:
                self.shoot(self.bullets_group, self.all_sprites, hero_pos_x, hero_pos_y)
                self.start_timer = pygame.time.get_ticks()
            print(self.start_timer)

    def shoot(self, bullets_group, all_sprites, pos_mouse_x, pos_mouse_y):

        speed_x, speed_y = find_enemy_speed(pos_mouse_x, pos_mouse_y, self.rect.centerx, self.rect.centery)

        bullet = EnemyBullet(self.rect.centerx - (BULLET_SIZE // 2),
                        self.rect.centery - (BULLET_SIZE // 2), speed_x, speed_y)
        bullets_group.add(bullet)
        all_sprites.add(bullet)
