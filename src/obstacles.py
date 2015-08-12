import pygame as pg
import math


COLOR_KEY = (255, 0, 255)

class Brick(pg.sprite.Sprite):
  def __init__(self, rect):
    pg.sprite.Sprite.__init__(self)
    self.rect = pg.Rect(rect)
    self.image = pg.Surface(self.rect.size).convert()
    self.image.set_colorkey(COLOR_KEY)

    self.size = 10

    brick_img = pg.image.load("assets/sprites/brick3.png").convert_alpha()

    for i in range(int(math.ceil(self.rect.width / self.size))):
      for j in range(int(math.ceil(self.rect.height / self.size))):
        self.image.blit(brick_img, (self.size * i, self.size * j))

    self.type = "normal"

class Pillar(pg.sprite.Sprite):
  def __init__(self, rect):
    pg.sprite.Sprite.__init__(self)
    self.rect = pg.Rect(rect)
    self.image = pg.Surface(self.rect.size).convert()
    self.image.set_colorkey(COLOR_KEY)

    self.size = 20

    brick_img = pg.image.load("assets/sprites/pillar.png").convert_alpha()

    for i in range(int(math.ceil(self.rect.width / self.size))):
      for j in range(int(math.ceil(self.rect.height / self.size))):
        self.image.blit(brick_img, (self.size * i, self.size * j))

    self.type = "normal"

