import pygame
from pygame import *


class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.image = Surface((20, 70))
        self.image.fill(Color('red'))
        self.rect = Rect(x, y, 20, 70)
        self.pos = (self.rect.x, self.rect.y)
        self.hp = 100

    def update(self, platforms):
        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        if not self.onGround:
            self.yvel += 0.35
        self.collide(self.yvel, platforms)
        self.collide(self.xvel, platforms)

    def collide(self, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
