import pygame as pg


class AI:
  def __init__(self, servant, obstacles, player):
    self.servant = servant
    self.obstacles = obstacles
    self.player = player

    self.keys_pressed = []
    
  def get_actions(self):
    key_presses = []
    if self.should_attack():
      key_presses.append(self.servant.DOWN_KEY)
    key_releases = []
    return key_presses, key_releases

  # check whether the AI should attack
  def should_attack(self):
    if self.servant.direction == self.servant.LEFT_KEY:
      if pg.Rect.colliderect(self.servant.attack_left_rect, self.player.rect):
        return True
    else:
      if pg.Rect.colliderect(self.servant.attack_right_rect, self.player.rect):
        return True
    return False
