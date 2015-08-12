import pygame as pg


class Menu(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self):
    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0

    self.done = False
    self.quit = False
    self.keys = pg.key.get_pressed()


  def reset(self):
    self.__init__()

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif self.keys[pg.K_r]:
        self.done = True
        self.quit = False

  def draw(self):
    self.screen.fill(Menu.BACKGROUND_COLOR)
    font = pg.font.Font(None, 28)
    text = font.render('Not implemented yet!', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.center = self.screen_rect.center
    self.screen.blit(text, textpos)

  def main_loop(self):
    pg.display.set_caption(Menu.CAPTION)
    while not self.done:
      self.event_loop()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)
    return self.quit

