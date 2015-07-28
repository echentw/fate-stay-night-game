import os
import sys
import pygame as pg

import control as ctrl

CAPTION = "My Game"
SCREEN_SIZE = (1000, 500)


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
  
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
  
    run_it = ctrl.Control()
    run_it.main_loop()
  
    pg.quit()
    sys.exit()
