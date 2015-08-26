import pygame as pg

from src.servants import archer as arc
from src.servants import saber as sab
from src.servants import caster as cas

class State:
  PLAY = 0
  PLAYER = 1
  BACK = 2

class Selection:
  SABER = 0
  ARCHER = 1
  CASTER = 2
  NAME = {
    0: 'Saber',
    1: 'Archer',
    2: 'Caster'
  }


class Menu(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size, mute=False):
    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.keys = pg.key.get_pressed()

    # handles what happens after the menu is exited
    self.done = False
    self.quit = False

    # player
    self.player_loc = (120, 570)
    self.player_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
    self.player = sab.Saber(self.player_keys, self.player_loc, mute)

    # control navigation
    self.state = State.PLAY
    self.player_selection = Selection.SABER
    self.default_color = (200, 200, 200)
    self.select_color  = (200, 0, 200)

    # decoration
    self.background = pg.image.load("assets/sprites/night.png").convert()
    self.excalibur_im = pg.image.load("assets/sprites/excalibur.png").convert()
    self.excalibur_im.set_colorkey((255, 0, 255))

    # sound
    self.mute = mute
    self.sound_switch = pg.mixer.Sound("assets/soundfx/menu_switch.wav")
    self.sound_select = pg.mixer.Sound("assets/soundfx/menu_select.wav")


  def reset(self, mute=False):
    self.__init__((self.screen_rect.width, self.screen_rect.height), mute)

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif self.keys[pg.K_UP]:
        if self.state != State.PLAY:
          self.state -= 1
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_DOWN]:
        if self.state != State.BACK:
          self.state += 1
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_RETURN]:
        if self.state == State.PLAY:
          self.done = True
          if not self.mute:
            self.sound_switch.play()
            self.sound_select.play()
        elif self.state == State.PLAYER:
          self.player_selection = (self.player_selection + 1) % 3
          if not self.mute:
            self.sound_switch.play()
        elif self.state == State.BACK:
          self.done = True
          if not self.mute:
            self.sound_switch.play()


  def draw(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.excalibur_im, (0, 0))

    font = pg.font.Font('assets/fonts/outline_pixel-7.ttf', 50)
    text = font.render('Fate/Stay Night Game', 1, (150, 150, 250))
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery - 30
    self.screen.blit(text, textpos)

    play_text_color   = self.default_color
    player_text_color = self.default_color
    back_text_color   = self.default_color
    if self.state == State.PLAY:
      play_text_color = self.select_color
    elif self.state == State.PLAYER:
      player_text_color = self.select_color
    elif self.state == State.BACK:
      back_text_color = self.select_color

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 24)
    text = font.render('Play', 1, play_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 30
    self.screen.blit(text, textpos)

    text = font.render('Servant: ' + Selection.NAME[self.player_selection], 1, player_text_color)
    textpos = text.get_rect()
    textpos.x = 325
    textpos.centery = self.screen_rect.centery + 60
    self.screen.blit(text, textpos)

    text = font.render('Back', 1, back_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 90
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 24)
    text = font.render('UP and DOWN to navigate, ENTER to toggle', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.bottomright = self.screen_rect.bottomright
    self.screen.blit(text, textpos)


  def initialize_player(self):
    if self.player_selection == Selection.SABER:
      self.player = sab.Saber(self.player_keys, self.player_loc, self.mute)
    elif self.player_selection == Selection.ARCHER:
      self.player = arc.Archer(self.player_keys, self.player_loc, self.mute)
    elif self.player_selection == Selection.CASTER:
      self.player = cas.Caster(self.player_keys, self.player_loc, self.mute)


  def main_loop(self):
    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)
    self.initialize_player()

