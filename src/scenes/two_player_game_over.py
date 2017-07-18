import pygame as pg

class State:
  MAIN_MENU = 1
  EXIT = 2


class GameOver(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size, winner, mute=False):
    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.keys = pg.key.get_pressed()

    # the winner to display
    self.winner = winner
    self.winner_image = None
    self.frame_id = 0
    self.animate_timer = 0.0
    self.animate_fps = 7.0
    self.frames = self.get_big_frames(self.winner)

    # handle player selection
    self.done = False
    self.quit = False

    # control navigation
    self.state = State.MAIN_MENU
    self.default_color = (200, 200, 200)
    self.select_color  = (250, 250, 0)

    # decoration
    self.background = pg.image.load("assets/sprites/blue.png").convert()

    # sound
    self.mute = mute
    self.sound_switch = pg.mixer.Sound("assets/soundfx/menu_switch.wav")
    self.sound_select = pg.mixer.Sound("assets/soundfx/menu_select.wav")



  def reset(self, winner, mute=False):
    self.__init__((self.screen_rect.width, self.screen_rect.height),
                  winner, mute)

  # helper method to get big walking frames
  def get_big_frames(self, servant):
    frames = [pg.transform.scale(servant.walk_frames[servant.LEFT_KEY][i],
        (servant.rect.width * 2, servant.rect.height * 2)) \
        for i in range(len(servant.walk_frames[servant.LEFT_KEY]))]
    return frames

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
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_DOWN]:
        if self.state != State.EXIT:
          self.state += 1
          if not self.mute:
            self.sound_switch.play()
      elif self.keys[pg.K_RETURN]:
        if self.state == State.MAIN_MENU:
          self.done = True
          if not self.mute:
            self.sound_switch.play()
            self.sound_select.play()
        elif self.state == State.EXIT:
          self.done = True

  def update(self):
    now = pg.time.get_ticks()
    if now - self.animate_timer > 1000 / self.animate_fps:
      self.animate_timer = now
      self.frame_id = (self.frame_id + 1) % len(self.frames)
    self.winner_image = self.frames[self.frame_id]

  def draw(self):
    self.screen.blit(self.background, (0, 0))

    self.screen.blit(self.winner_image,
                     (self.screen_rect.centerx - self.winner.rect.width,
                      self.screen_rect.centery - 200))

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
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

