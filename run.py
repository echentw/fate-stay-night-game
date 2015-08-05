import os
import sys
import pygame as pg

from src import control as ctrl

CAPTION = "My Game"
SCREEN_SIZE = (500, 500)


if __name__ == "__main__":
  os.environ['SDL_VIDEO_CENTERED'] = '1'

  pg.init()
  pg.display.set_caption(CAPTION)
  pg.display.set_mode(SCREEN_SIZE)

  run_it = ctrl.Control((1000, 1000))
  run_it.main_loop()

  pg.quit()
  sys.exit()

