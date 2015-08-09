import os
import sys
import pygame as pg

import control as ctrl
import main_menu


class Game:
  CAPTION = "My Game"
  SCREEN_SIZE = (800, 800)

  def __init__(self):
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    pg.display.set_caption(Game.CAPTION)
    pg.display.set_mode(Game.SCREEN_SIZE)

    self.menu = main_menu.Menu(Game.SCREEN_SIZE)
    self.run_it = ctrl.Control((1000, 1000))

  def start(self):
    self.menu.main_loop()
    self.run_it.main_loop()

