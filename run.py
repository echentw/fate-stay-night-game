import os
import sys
import pygame as pg

from src import control as ctrl
from src import main_menu

CAPTION = "My Game"
SCREEN_SIZE = (800, 800)


if __name__ == "__main__":
  os.environ['SDL_VIDEO_CENTERED'] = '1'

  pg.init()
  pg.display.set_caption(CAPTION)
  pg.display.set_mode(SCREEN_SIZE)

  menu = main_menu.Menu(SCREEN_SIZE)
  menu.main_loop()

  run_it = ctrl.Control((1000, 1000))
  run_it.main_loop()

  pg.quit()
  sys.exit()

