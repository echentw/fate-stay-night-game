import os
import pygame as pg

import game
import main_menu
import game_over


class Control:
  CAPTION = "My Game"
  SCREEN_SIZE = (800, 800)

  def __init__(self):
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    pg.display.set_caption(Control.CAPTION)
    pg.display.set_mode(Control.SCREEN_SIZE)

    self.menu = main_menu.Menu(Control.SCREEN_SIZE)
    self.game = game.Game((1000, 1000))
    self.game_over = game_over.GameOver(Control.SCREEN_SIZE)


  def start(self):
    while True:
      self.menu.reset()
      self.game.reset()
      self.game_over.reset()

      quit = self.menu.main_loop()
      if quit:
        break

      quit = self.game.main_loop()
      if quit:
        break

      self.game_over.set_winner(self.game.winner)
      quit = self.game_over.main_loop()
      if quit:
        break

