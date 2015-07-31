import os
import sys
import pygame as pg

import saber as sab
import block

class Control(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  """Being controlling is our job."""
  def __init__(self):
    """Initialize standard attributes, standardly."""
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.done = False
    self.keys = pg.key.get_pressed()

    x = self.screen_rect.center[0] - 40
    y = self.screen_rect.center[1] + 40
    self.saber = sab.Saber("assets/saber_walk.png", (x,y,38,54),
                           "assets/saber_slash.png", (x,y,73,48), 3)

    self.obstacles = self.make_obstacles()

  def make_obstacles(self):
    walls = [block.Block(pg.Color("darkgreen"), (0, self.screen_rect.bottom - 20, self.screen_rect.width, 20)),
             block.Block(pg.Color("darkblue"), (0, 0, 20, self.screen_rect.height)),
             block.Block(pg.Color("darkred"), (self.screen_rect.width - 20, 0, 20, self.screen_rect.height))]

    static = [block.Block(pg.Color("blue"), (0, self.screen_rect.bottom - 60, self.screen_rect.width / 2, 20)),
              block.Block(pg.Color("green"), (0, self.screen_rect.bottom - 150, self.screen_rect.width / 2, 20))]

    return pg.sprite.Group(walls, static)

  def event_loop(self):
    """Add/pop directions from player's direction stack as necessary."""
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
      elif event.type == pg.KEYDOWN:
        self.saber.handle_keydown(event.key, self.obstacles)
      elif event.type == pg.KEYUP:
        self.saber.handle_keyup(event.key)

  def update(self):
    self.saber.update(self.screen_rect, self.obstacles)

  def draw(self):
    self.screen.fill(Control.BACKGROUND_COLOR)
    self.obstacles.draw(self.screen)
    self.saber.draw(self.screen)

  def main_loop(self):
    """Our main game loop; I bet you'd never have guessed."""
    pg.display.set_caption(Control.CAPTION)
    while not self.done:
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

