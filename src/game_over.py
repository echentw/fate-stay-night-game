import pygame as pg


class GameOver(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size):
    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.keys = pg.key.get_pressed()

    # the winner to display
    self.winner = None

    # handle player selection
    self.done = False
    self.quit = False


  def reset(self):
    self.__init__((self.screen_rect.width, self.screen_rect.height))

  def set_winner(self, winner):
    self.winner = winner

  # check for key presses
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif self.keys[pg.K_r]:
        self.done = True
        self.quit = False

  def update(self):
    pass

  def draw(self):
    font = pg.font.Font(None, 48)
    text1 = font.render(self.winner.name + " wins!", 1, (230, 230, 230))
    textpos1 = text1.get_rect()
    textpos1.centerx = self.screen.get_rect().centerx
    textpos1.centery = self.screen.get_rect().centery

    font = pg.font.Font(None, 24)
    text2 = font.render("Press esc to quit", 1, (230, 230, 230))
    textpos2 = text2.get_rect()
    textpos2.centerx = self.screen.get_rect().centerx
    textpos2.centery = self.screen.get_rect().centery + 40

    font = pg.font.Font(None, 24)
    text3 = font.render("Press r to go back to main menu", 1, (230, 230, 230))
    textpos3 = text3.get_rect()
    textpos3.centerx = self.screen.get_rect().centerx
    textpos3.centery = self.screen.get_rect().centery + 70

    self.screen.fill(GameOver.BACKGROUND_COLOR)
    self.screen.blit(text1, textpos1)
    self.screen.blit(text2, textpos2)
    self.screen.blit(text3, textpos3)


  def main_loop(self):
    pg.display.set_caption(GameOver.CAPTION)
    while not self.done:
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)
    return self.quit

