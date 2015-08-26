import pygame as pg


class AI:
  def __init__(self, servant, obstacles, player):
    self.servant = servant
    self.obstacles = obstacles
    self.player = player

    # [0] is the current moving direction, [1] is old
    self.move = {
      self.servant.LEFT_KEY: [False, False],
      self.servant.RIGHT_KEY: [False, False]
    }

    self.keys_pressed = []
    self.time = pg.time.get_ticks()


  def get_actions(self):
    key_presses = []
    if self.should_attack():
      key_presses.append(self.servant.DOWN_KEY)
      self.time = pg.time.get_ticks()
    if self.servant.direction == self.servant.LEFT_KEY:
      if self.can_move_left():
        key_presses.append(self.servant.LEFT_KEY)
        self.move_left()
      elif self.can_move_right():
        key_presses.append(self.servant.RIGHT_KEY)
        self.move_right()
    else:
      if self.can_move_right():
        key_presses.append(self.servant.RIGHT_KEY)
        self.move_right()
      elif self.can_move_left():
        key_presses.append(self.servant.LEFT_KEY)
        self.move_left()


    key_releases = []
    if self.stopped_moving_left():
      key_releases.append(self.servant.LEFT_KEY)
    if self.stopped_moving_right():
      key_releases.append(self.servant.RIGHT_KEY)

    return key_presses, key_releases


  def should_attack(self):
    return pg.Rect.colliderect(self.servant.rect, self.player.rect)

  def can_move_left(self):
    # check for wall on left
    self.servant.rect.move_ip((-5, 0))
    col_left = pg.sprite.spritecollide(self.servant, self.obstacles, False)
    self.servant.rect.move_ip((5, 0))

    # check for ground on left
    self.servant.rect.move_ip((-15, 1))
    col_below = pg.sprite.spritecollide(self.servant, self.obstacles, False)
    self.servant.rect.move_ip((15, -1))

    return not col_left and col_below


  def can_move_right(self):
    # check for wall on left
    self.servant.rect.move_ip((5, 0))
    col_right = pg.sprite.spritecollide(self.servant, self.obstacles, False)
    self.servant.rect.move_ip((-5, 0))

    # check for ground on left
    self.servant.rect.move_ip((15, 1))
    col_below = pg.sprite.spritecollide(self.servant, self.obstacles, False)
    self.servant.rect.move_ip((-15, -1))

    return not col_right and col_below


  def move_left(self):
    self.move[self.servant.LEFT_KEY][1] = self.move[self.servant.LEFT_KEY][0]
    self.move[self.servant.RIGHT_KEY][1] = self.move[self.servant.RIGHT_KEY][0]
    self.move[self.servant.LEFT_KEY][0] = True
    self.move[self.servant.RIGHT_KEY][0] = False

  def move_right(self):
    self.move[self.servant.LEFT_KEY][1] = self.move[self.servant.LEFT_KEY][0]
    self.move[self.servant.RIGHT_KEY][1] = self.move[self.servant.RIGHT_KEY][0]
    self.move[self.servant.LEFT_KEY][0] = False
    self.move[self.servant.RIGHT_KEY][0] = True

  def stopped_moving_left(self):
    return self.move[self.servant.LEFT_KEY][0] == False and \
           self.move[self.servant.LEFT_KEY][1] == True

  def stopped_moving_right(self):
    return self.move[self.servant.RIGHT_KEY][0] == False and \
           self.move[self.servant.RIGHT_KEY][1] == True
