import pygame as pg

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
    self.quit = False
    self.keys = pg.key.get_pressed()

    self.player1_location = (800, 200)
    self.player2_location = (200, 200)

    self.player1_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
    self.player2_keys = (pg.K_w, pg.K_s, pg.K_a, pg.K_d)

    self.player1 = sab.Saber(self.player1_keys, self.player1_location)
    self.player2 = arc.Archer(self.player2_keys, self.player2_location)


  def reset(self):
    self.__init__((self.screen_rect.width, self.screen_rect.height))

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif self.keys[pg.K_SPACE]:
        self.done = True
        self.quit = False

      # player 1 selection
      elif self.keys[pg.K_LEFT]:
        self.player1 = sab.Saber(self.player1_keys, self.player1_location)
      elif self.keys[pg.K_DOWN]:
        self.player1 = arc.Archer(self.player1_keys, self.player1_location)
      elif self.keys[pg.K_RIGHT]:
        self.player1 = cast.Caster(self.player1_keys, self.player1_location)

      # player 2 selection
      elif self.keys[pg.K_a]:
        self.player2 = sab.Saber(self.player2_keys, self.player2_location)
      elif self.keys[pg.K_s]:
        self.player2 = arc.Archer(self.player2_keys, self.player2_location)
      elif self.keys[pg.K_d]:
        self.player2 = cast.Caster(self.player2_keys, self.player2_location)


  def update(self):
    pass

  # draw things onto the screen
  def draw(self):
    self.screen.fill(Menu.BACKGROUND_COLOR)
    self.screen.blit(self.screen, (0, 0), self.screen_rect)

    font = pg.font.Font(None, 64)
    text = font.render('Fate/Stay Night Game', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery - 30
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 24)
    text = font.render('Player 1 selection: press LEFT for Saber, DOWN for Archer, RIGHT for Caster (default = Archer)', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.x = 30
    textpos.centery = self.screen_rect.centery + 30
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 24)
    text = font.render('Player 2 selection: press \'a\' for saber, \'s\' for archer, \'d\' for caster                          (default = Saber)', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.x = 30
    textpos.centery = self.screen_rect.centery + 60
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 36)
    text = font.render('Press Space to play', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 110
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
    return self.quit

