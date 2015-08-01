import os
import sys
import pygame as pg

import archer as arch
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
#    self.saber = sab.Saber(3, "assets/sprites/saber_walk.png", (x,y,38,54),
#                              "assets/sprites/saber_slash.png", (x,y,73,48),
#                              "assets/sprites/saber_jump1.png", (x,y,38,58),
#                              "assets/sprites/saber_jump2.png", (x,y,41,63))
    self.saber = arch.Archer(3, "assets/sprites/archer_walk.png", (x,y,33,60),
                                "assets/sprites/archer_slash.png", (x,y,90,66),
                                "assets/sprites/archer_jump1.png", (x,y,52,59),
                                "assets/sprites/archer_jump2.png", (x,y,52,59))
    self.obstacles = self.make_obstacles()

  def make_obstacles(self):
#    walls = [block.Block(pg.Color("darkgreen"), (0, self.screen_rect.bottom - 20, self.screen_rect.width, 20)),
#             block.Block(pg.Color("darkblue"), (0, 0, 20, self.screen_rect.height)),
#             block.Block(pg.Color("darkred"), (self.screen_rect.width - 20, 0, 20, self.screen_rect.height))]
#
#    static = [block.Block(pg.Color("blue"), (0, self.screen_rect.bottom - 60, self.screen_rect.width / 2, 20)),
#              block.Block(pg.Color("green"), (0, self.screen_rect.bottom - 150, self.screen_rect.width / 2, 20))]

    walls = [block.Block(pg.Color("chocolate"), (0,980,1000,20)),
             block.Block(pg.Color("chocolate"), (0,0,20,1000)),
             block.Block(pg.Color("chocolate"), (980,0,20,1000))]
    static = [block.Block(pg.Color("darkgreen"), (250,780,200,100)),
              block.Block(pg.Color("darkgreen"), (600,880,200,100)),
              block.Block(pg.Color("darkgreen"), (20,360,880,40)),
              block.Block(pg.Color("darkgreen"), (950,400,30,20)),
              block.Block(pg.Color("darkgreen"), (20,630,50,20)),
              block.Block(pg.Color("darkgreen"), (80,530,50,20)),
              block.Block(pg.Color("darkgreen"), (130,470,200,215)),
              block.Block(pg.Color("darkgreen"), (20,760,30,20)),
              block.Block(pg.Color("darkgreen"), (400,740,30,40))]

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
    self.screen_rect.center = self.saber.rect.center

  def draw(self):
    level = pg.Surface((1000,1000)).convert()
    level.fill(Control.BACKGROUND_COLOR)
    level_rect = level.get_rect()
    self.screen_rect.clamp_ip(level_rect)
    self.obstacles.draw(level)
    self.saber.draw(level)
    self.screen.blit(level, (0, 0), self.screen_rect)

#    self.screen.fill(Control.BACKGROUND_COLOR)
#    self.obstacles.draw(self.screen)
#    self.saber.draw(self.screen)

  def main_loop(self):
    """Our main game loop; I bet you'd never have guessed."""
    pg.display.set_caption(Control.CAPTION)
#    pg.display.toggle_fullscreen()
    pg.mixer.music.load("assets/music/oath-sign-orchestra.mp3")
    pg.mixer.music.play()

    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

