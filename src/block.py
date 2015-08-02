import pygame as pg
import math
import random

class Block(pg.sprite.Sprite):
  def __init__(self, color, rect):
    pg.sprite.Sprite.__init__(self)
    self.rect = pg.Rect(rect)
    self.image = pg.Surface(self.rect.size).convert()
    self.image.fill(color)
    
    brick_img = pg.image.load("assets/sprites/brick3.png").convert_alpha()
    brick2_img = pg.image.load("assets/sprites/brick2.png").convert_alpha()
    for i in range(int(math.ceil(self.rect.width / 10))):
      for j in range(int(math.ceil(self.rect.height / 10))):
        if random.random() < 0.2:
          self.image.blit(brick_img, (10 * i, 10 * j))
        else:
          self.image.blit(brick2_img, (10 * i, 10 * j))

    self.type = "normal"
