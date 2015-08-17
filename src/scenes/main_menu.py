import pygame as pg

from src.servants import archer as arc
from src.servants import saber as sab
from src.servants import caster as cast
from src.servants import assassin as ass

class State:
  SINGLE_PLAYER = 0
  TWO_PLAYER = 1
  SOUND = 2
  EXIT = 3


class Menu(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size, mute=False):
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock = pg.time.Clock()
    self.fps = 60.0
    self.keys = pg.key.get_pressed()

    self.done = False
    self.quit = False

    # control main menu screen navigation
    self.state = State.SINGLE_PLAYER
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


  def reset(self):
    self.__init__((self.screen_rect.width, self.screen_rect.height), self.mute)

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif self.keys[pg.K_UP]:
        if self.state != State.SINGLE_PLAYER:
          self.state -= 1
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_DOWN]:
        if self.state != State.EXIT:
          self.state += 1
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_RETURN]:
        if self.state == State.SINGLE_PLAYER or self.state == State.TWO_PLAYER:
          self.done = True
          if not self.mute:
            self.sound_switch.play()
            self.sound_select.play()
        elif self.state == State.SOUND:
          self.mute = not self.mute
          if self.mute:
            pg.mixer.music.set_volume(0.0)
            self.mute = True
          else:
            pg.mixer.music.set_volume(1.0)
            self.mute = False
            self.sound_switch.play()
        elif self.state == State.EXIT:
          self.done = True


  # draw things onto the screen
  def draw(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.excalibur_im, (0, 0))

    font = pg.font.Font('assets/fonts/outline_pixel-7.ttf', 50)
    text = font.render('Fate/Stay Night Game', 1, (150, 150, 250))
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery - 30
    self.screen.blit(text, textpos)

    singleplayer_text_color = self.default_color
    multiplayer_text_color  = self.default_color
    sound_text_color        = self.default_color
    exit_text_color         = self.default_color
    if self.state == State.SINGLE_PLAYER:
      singleplayer_text_color = self.select_color
    elif self.state == State.TWO_PLAYER:
      multiplayer_text_color = self.select_color
    elif self.state == State.SOUND:
      sound_text_color = self.select_color
    elif self.state == State.EXIT:
      exit_text_color = self.select_color

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 24)
    text = font.render('Single Player', 1, singleplayer_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 30
    self.screen.blit(text, textpos)

    text = font.render('Multi Player', 1, multiplayer_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 60
    self.screen.blit(text, textpos)

    text = font.render('Sound: ' + get_str(self.mute), 1, sound_text_color)
    textpos = text.get_rect()
    textpos.x = 375
    textpos.centery = self.screen_rect.centery + 90
    self.screen.blit(text, textpos)

    text = font.render('Exit', 1, exit_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 120
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 24)
    text = font.render('UP and DOWN to navigate, ENTER to toggle', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.bottomright = self.screen_rect.bottomright
    self.screen.blit(text, textpos)


  # main loop of the game
  def main_loop(self):
    while not self.done:
      if self.mute and not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

def get_str(mute):
  if mute:
    return 'OFF'
  else:
    return 'ON'

