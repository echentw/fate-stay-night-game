import pygame as pg

class Block(pg.sprite.Sprite):
  def __init__(self, color, rect):
    pg.sprite.Sprite.__init__(self)
    self.rect = pg.Rect(rect)
    self.image = pg.Surface(self.rect.size).convert()
    self.image.fill(color)
    self.type = "normal"
