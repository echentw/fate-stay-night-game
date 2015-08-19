import pygame as pg

from src import maps


class Game(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, level_size, player1, player2, mute=False):
    # winner is set when one player's health hits 0
    self.winner = None

    # the entire map
    self.level = pg.Surface((level_size[0], level_size[1])).convert()
    self.level_rect = self.level.get_rect()

    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0

    self.done = False
    self.quit = False
    self.keys = pg.key.get_pressed()

    # sound when an attack hits
    self.mute = mute
    self.sound_impact = pg.mixer.Sound("assets/soundfx/hit.wav")

    # initialize the players
    self.player1 = player1
    self.player2 = player2

    # initialize the obstacles of the game
    self.obstacles, self.fake_obstacles = maps.get_simple_map()
    self.player1_obstacles = pg.sprite.Group(self.player2)
    self.player1_obstacles.add(self.obstacles)
    self.player2_obstacles = pg.sprite.Group(self.player1)
    self.player2_obstacles.add(self.obstacles)

    # initialize the face images of the characters
    self.player2.face_im = pg.transform.flip(self.player2.face_im, True, False)
    self.player1_face_rect = self.player1.face_im.get_rect()
    self.player1_face_rect.right = self.screen_rect.width
    self.player2_face_rect = self.player2.face_im.get_rect()


  def reset(self, player1, player2, mute=False):
    self.__init__((self.level_rect.width, self.level_rect.height),
                  player1, player2, mute)

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()

      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True

      # someone is attacking
      elif event.type == pg.KEYDOWN:
        if event.key == self.player1.DOWN_KEY:
          if not self.player1.attacking and not self.player1.hurt:
            if self.player1.direction == self.player1.LEFT_KEY:
              if self.player2.receive_attack(self.player2.RIGHT_KEY,
                                             self.player1.attack_left_rect):
                if not self.mute:
                  self.sound_impact.play()
            else:
              if self.player2.receive_attack(self.player2.LEFT_KEY,
                                             self.player1.attack_right_rect):
                if not self.mute:
                  self.sound_impact.play()
        elif event.key == self.player2.DOWN_KEY:
          if not self.player2.attacking and not self.player2.hurt:
            if self.player2.direction == self.player2.LEFT_KEY:
              if self.player1.receive_attack(self.player1.RIGHT_KEY,
                                             self.player2.attack_left_rect):
                if not self.mute:
                  self.sound_impact.play()
            else:
              if self.player1.receive_attack(self.player1.LEFT_KEY,
                                             self.player2.attack_right_rect):
                if not self.mute:
                  self.sound_impact.play()
        self.player1.handle_keydown(event.key, self.player1_obstacles)
        self.player2.handle_keydown(event.key, self.player2_obstacles)

      elif event.type == pg.KEYUP:
        self.player1.handle_keyup(event.key)
        self.player2.handle_keyup(event.key)

  # check for winner, update player position
  def update(self):
    if self.player1.health == 0:
      self.winner = self.player2
      self.done = True
      self.quit = False
    elif self.player2.health == 0:
      self.winner = self.player1
      self.done = True
      self.quit = False
    self.player1.update(self.screen_rect, self.player1_obstacles)
    self.player2.update(self.screen_rect, self.player2_obstacles)
    self.screen_rect.center = \
        ((self.player1.rect.center[0] + self.player2.rect.center[0]) / 2.0,
         (self.player1.rect.center[1] + self.player2.rect.center[1]) / 2.0)

  # draw things onto the screen
  def draw(self):
    self.level.fill(Game.BACKGROUND_COLOR)
    self.screen_rect.clamp_ip(self.level_rect)
    self.obstacles.draw(self.level)
    self.player1.draw(self.level)
    self.player2.draw(self.level)
    self.fake_obstacles.draw(self.level)
    self.screen.blit(self.level, (0, 0), self.screen_rect)

    self.screen.blit(self.player1.face_im, self.player1_face_rect)
    self.screen.blit(self.player2.face_im, self.player2_face_rect)

    font = pg.font.Font(None, 28)
    name = font.render(self.player1.name, 1, (200, 200, 200))
    health = font.render(get_health_bar(self.player1), 1, (200, 200, 200))
    textpos = name.get_rect()
    textpos.topleft = self.player1_face_rect.topleft
    self.screen.blit(name, textpos)
    textpos.y = textpos.y + 12
    self.screen.blit(health, textpos)

    name = font.render(self.player2.name, 2, (200, 200, 200))
    health = font.render(get_health_bar(self.player2), 1, (200, 200, 200))
    textpos = name.get_rect()
    textpos.topleft = self.player2_face_rect.topleft
    self.screen.blit(name, textpos)
    textpos.y = textpos.y + 12
    self.screen.blit(health, textpos)


  # main loop of the game
  def main_loop(self):
    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)


# Hacky way to show the health bar
def get_health_bar(player):
  output = ''
  for i in xrange(player.health):
    output += '--'
  return output

