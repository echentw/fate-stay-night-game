import pygame as pg

from src import obstacles as ob

from src.servants import assassin as ass


class Game(object):
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, level_size, player, mute=False):
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

    # initialize the player and npcs
    self.player = player
    self.npcs = self.get_npcs();

    # initialize the obstacles of the game
    self.obstacles, self.fake_obstacles = self.make_obstacles()
    self.player_obstacles = pg.sprite.Group(self.obstacles)

    # initialize the face image of the character
    self.player.face_im = pg.transform.flip(self.player.face_im, True, False)
    self.player_face_rect = self.player.face_im.get_rect()


  def reset(self, player, mute=False):
    self.__init__((self.level_rect.width, self.level_rect.height),
                  player, mute)

  # helper method to initialize the npcs
  def get_npcs(self):
    npcs = [
      ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d), (800, 200), self.mute),
      ass.Assassin((pg.K_w, pg.K_s, pg.K_a, pg.K_d), (880, 200), self.mute)
    ]
    return npcs

  # helper method to create the platforms in the game
  def make_obstacles(self):
    size = 20

    walls = [ob.Brick((0 * size, 48 * size, 50 * size, 2 * size)),
             ob.Brick((0 * size, 0 * size, 50 * size, 2 * size)),
             ob.Brick((0 * size, 0 * size, 3 * size, 50 * size)),
             ob.Brick((47 * size, 0 * size, 3 * size, 50 * size))]

    ground = [ob.Brick((1 * size, 42 * size, 32 * size, 6 * size)),
              ob.Brick((1 * size, 36 * size, 17 * size, 6 * size))]

    big = [ob.Brick((5 * size, 18 * size, 9 * size, 13 * size)),
           ob.Brick((4 * size, 23 * size, 1 * size, 1 * size)),
           ob.Brick((4 * size, 30 * size, 1 * size, 1 * size)),
           ob.Brick((14 * size, 23 * size, 1 * size, 1 * size)),
           ob.Brick((14 * size, 30 * size, 1 * size, 1 * size))]

    floating = [ob.Brick((20 * size, 21 * size, 9 * size, 2 * size)),
                ob.Brick((23 * size, 31 * size, 15 * size, 1 * size)),
                ob.Brick((33 * size, 19 * size, 1 * size, 1 * size)),
                ob.Brick((37 * size, 16 * size, 7 * size, 2 * size))]

    high = [ob.Brick((6 * size, 9 * size, 3 * size, 2 * size)),
            ob.Brick((15 * size, 9 * size, 3 * size, 2 * size)),
            ob.Brick((24 * size, 9 * size, 3 * size, 2 * size)),
            ob.Brick((33 * size, 9 * size, 3 * size, 2 * size))]

    high_pillars = [ob.Pillar((6 * size, 8 * size, 3 * size, 1 * size)),
                    ob.Pillar((15 * size, 8 * size, 3 * size, 1 * size)),
                    ob.Pillar((24 * size, 8 * size, 3 * size, 1 * size)),
                    ob.Pillar((33 * size, 8 * size, 3 * size, 1 * size))]

    floating_pillars = [ob.Pillar((20 * size, 20 * size, 9 * size, 1 * size)),
                        ob.Pillar((23 * size, 30 * size, 15 * size, 1 * size)),
                        ob.Pillar((37 * size, 15 * size, 7 * size, 1 * size))]

    return (pg.sprite.Group(walls, ground, big, floating, high),
            pg.sprite.Group(high_pillars, floating_pillars))

  # check for key presses and releases
  def event_loop(self):
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
                if npc.receive_attack(npc.RIGHT_KEY,
                                      self.player.attack_left_rect):
                  if not self.mute:
                    self.sound_impact.play()
            else:
              for npc in self.npcs:
                if npc.receive_attack(npc.LEFT_KEY,
                                      self.player.attack_right_rect):
                  if not self.mute:
                    self.sound_impact.play()
        self.player.handle_keydown(event.key, self.player_obstacles)

      elif event.type == pg.KEYUP:
        self.player.handle_keyup(event.key)


  # check for winner, update player position
  def update(self):
    if self.player.health == 0:
      self.done = True
      self.quit = False
    for npc in self.npcs:
      if npc.health == 0:
        self.npcs.remove(npc)
    if not self.npcs:
      self.done = True
      self.quit = False
    self.player.update(self.screen_rect, self.player_obstacles)
    for npc in self.npcs:
      npc.update(self.screen_rect, self.player_obstacles)
    self.screen_rect.center = self.player.rect.center

  # draw things onto the screen
  def draw(self):
    self.level.fill(Game.BACKGROUND_COLOR)
    self.screen_rect.clamp_ip(self.level_rect)
    self.obstacles.draw(self.level)
    for npc in self.npcs:
      npc.draw(self.level)
    self.player.draw(self.level)
    self.fake_obstacles.draw(self.level)
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
  for i in xrange(player.health):
    output += '--'
  return output

