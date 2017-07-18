import pygame as pg

from src import maps
from src import ai
from src import obstacles as ob

from src.servants import assassin as ass


class Game(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, level_size, player, mute=False):
    # whether the player wins or loses
    self.win = False

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

    # initialize the obstacles of the game
    self.obstacles, self.fake_obstacles = maps.get_complex_map()
    self.player_obstacles = pg.sprite.Group(self.obstacles)
    self.holy_grail = pg.sprite.Group(ob.HolyGrail((1160, 166, 30, 32)))

    # initialize the player and npcs
    self.player = player
    self.npcs = self.get_npcs();

    # initialize the face image of the character
    self.player.face_im = pg.transform.flip(self.player.face_im, True, False)
    self.player_face_rect = self.player.face_im.get_rect()


  def reset(self, player, mute=False):
    self.__init__((self.level_rect.width, self.level_rect.height),
                  player, mute)

  # helper method to initialize the npcs
  def get_npcs(self):
    npcs = [
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (520, 575), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (170, 315), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (800, 200), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (395, 135), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (255, 135), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (1255, 455), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (1238, 295), self.mute, direction=2),
            self.player_obstacles,
            self.player),
      ai.AI(ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                (1458, 195), self.mute, direction=2),
            self.player_obstacles,
            self.player)
    ]
    return npcs

  # check for key presses and releases
  def event_loop(self):
    # npc actions
    for npc in self.npcs:
      key_presses, key_releases = npc.get_actions()
      for key in key_presses:
        if key == npc.servant.DOWN_KEY:
          if not npc.servant.attacking and not npc.servant.hurt:
            if npc.servant.direction == npc.servant.LEFT_KEY:
              if self.player.receive_attack(self.player.RIGHT_KEY,
                                            npc.servant.attack_left_rect):
                if not self.mute:
                  self.sound_impact.play()
            else:
              if self.player.receive_attack(self.player.LEFT_KEY,
                                            npc.servant.attack_right_rect):
                if not self.mute:
                  self.sound_impact.play()
        npc.servant.handle_keydown(key, self.player_obstacles)
      for key in key_releases:
        npc.servant.handle_keyup(key)

    # player actions
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True
      elif event.type == pg.KEYDOWN:
        if event.key == self.player.DOWN_KEY:
          if not self.player.attacking and not self.player.hurt:
            if self.player.direction == self.player.LEFT_KEY:
              for npc in self.npcs:
                if npc.servant.receive_attack(npc.servant.RIGHT_KEY,
                                              self.player.attack_left_rect):
                  if not self.mute:
                    self.sound_impact.play()
            else:
              for npc in self.npcs:
                if npc.servant.receive_attack(npc.servant.LEFT_KEY,
                                              self.player.attack_right_rect):
                  if not self.mute:
                    self.sound_impact.play()
        self.player.handle_keydown(event.key, self.player_obstacles)
      elif event.type == pg.KEYUP:
        self.player.handle_keyup(event.key)


  # check for winner, update player position
  def update(self):
    if pg.sprite.spritecollide(self.player, self.holy_grail, False):
      self.done = True
      self.quit = False
      self.win = True
    for npc in self.npcs:
      if npc.servant.health <= 0:
        self.npcs.remove(npc)
    if self.player.health <= 0:
      self.done = True
      self.quit = False
      self.win = False
    self.player.update(self.screen_rect, self.player_obstacles)
    for npc in self.npcs:
      npc.servant.update(self.screen_rect, self.player_obstacles)
    self.screen_rect.center = self.player.rect.center

  # draw things onto the screen
  def draw(self):
    self.level.fill(Game.BACKGROUND_COLOR)
    self.screen_rect.clamp_ip(self.level_rect)
    self.obstacles.draw(self.level)
    for npc in self.npcs:
      npc.servant.draw(self.level)
    self.player.draw(self.level)
    self.fake_obstacles.draw(self.level)
    self.holy_grail.draw(self.level)
    self.screen.blit(self.level, (0, 0), self.screen_rect)

    self.screen.blit(self.player.face_im, self.player_face_rect)

    font = pg.font.Font(None, 28)
    name = font.render(self.player.name, 1, (200, 200, 200))
    health = font.render(get_health_bar(self.player), 1, (200, 200, 200))
    textpos = name.get_rect()
    textpos.topleft = self.player_face_rect.topleft
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
  for i in range(player.health):
    output += '--'
  return output

