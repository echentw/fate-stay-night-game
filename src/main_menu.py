import os
import sys
import pygame as pg

import player
import archer as arc
import saber as sab
import caster as cast

class Menu(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size):
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock = pg.time.Clock()
    self.fps = 60.0
    self.done = False
    self.keys = pg.key.get_pressed()

    # controls for the players
    player1_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
    player2_keys = (pg.K_w, pg.K_s, pg.K_a, pg.K_d)

    # initialize characters
    saber_location = (500, 500)
    archer_location = (800, 200)
    caster_location = (200, 200)
    saber = sab.Saber(player1_keys, saber_location)
    archer = arc.Archer(player2_keys, archer_location)
    caster = cast.Caster(player2_keys, caster_location)

    # initialize the players
    self.player1 = None
    self.player2 = None

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True

  # check for winner, update player position
  def update(self):
    pass

  # draw things onto the screen
  def draw(self):
    self.screen.fill(Menu.BACKGROUND_COLOR)
    self.screen.blit(self.screen, (0, 0), self.screen_rect)

    font = pg.font.Font(None, 28)
    text = font.render('Fate/Stay Night Game', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.center = self.screen_rect.center
    self.screen.blit(text, textpos)

  # main loop of the game
  def main_loop(self):
    pg.display.set_caption(Menu.CAPTION)
    while not self.done:
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

