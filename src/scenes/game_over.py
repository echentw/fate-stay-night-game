import pygame as pg

class State:
  MAIN_MENU = 1
  EXIT = 2


class GameOver(object):
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

    # control navigation
    self.state = State.MAIN_MENU
    self.default_color = (200, 200, 200)
    self.select_color  = (250, 250, 0)

    # decoration
    self.background = pg.image.load("assets/sprites/ubw.png").convert()


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
      elif self.keys[pg.K_UP]:
        if self.state != State.MAIN_MENU:
          self.state -= 1
      elif self.keys[pg.K_DOWN]:
        if self.state != State.EXIT:
          self.state += 1
      elif self.keys[pg.K_RETURN]:
        if self.state == State.MAIN_MENU:
          self.done = True
          self.quit = False
        elif self.state == State.EXIT:
          self.done = True
          self.quit = True

  def update(self):
    pass

  def draw(self):
    self.screen.blit(self.background, (0, 0))

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 48)
    text = font.render(self.winner.name + " wins!", 1, (230, 230, 230))
    textpos = text.get_rect()
    textpos.centerx = self.screen.get_rect().centerx
    textpos.centery = self.screen.get_rect().centery - 30
    self.screen.blit(text, textpos)

    main_menu_text_color = self.default_color
    exit_text_color      = self.default_color
    if self.state == State.MAIN_MENU:
      main_menu_text_color = self.select_color
    elif self.state == State.EXIT:
      exit_text_color = self.select_color

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 24)
    text = font.render('Main Menu', 1, main_menu_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 30
    self.screen.blit(text, textpos)

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 24)
    text = font.render('Exit', 1, exit_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 60
    self.screen.blit(text, textpos)


  def main_loop(self):
    while not self.done:
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

