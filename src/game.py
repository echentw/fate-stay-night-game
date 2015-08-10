import os
import pygame as pg

import control as ctrl
import main_menu
import game_over


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
    self.game_over = game_over.GameOver(Game.SCREEN_SIZE)


  def start(self):
    while True:
      self.menu.reset()
      self.run_it.reset()
      self.game_over.reset()

      quit = self.menu.main_loop()
      if quit:
        break

      quit = self.run_it.main_loop()
      if quit:
        break

      self.game_over.set_winner(self.run_it.winner)
      quit = self.game_over.main_loop()
      if quit:
        break

