import pygame as pg

from src import player


class Archer(player.Player):
  def __init__(self, keys, start_location, mute=False):
    player.Player.__init__(self, keys, mute)

    # qualities
    self.name = 'Archer'
    self.health = 3
    self.max_speed = 6
    self.agility = 1
    self.jump_power = 12.0

    # files used
    face_im      = "assets/sprites/archer_face.png"
    walk_im      = "assets/sprites/archer_walk.png"
    attack_im    = "assets/sprites/archer_slash.png"
    jump_up_im   = "assets/sprites/archer_jump1.png"
    jump_down_im = "assets/sprites/archer_jump2.png"
    hurt_im      = "assets/sprites/archer_hurt.png"
    attack_sound = "assets/soundfx/woosh.wav"
    land_sound   = "assets/soundfx/thud.wav"

    # bounding boxes for each image
    rect           = (start_location[0], start_location[1], 33, 60)
    attack_rect    = (start_location[0], start_location[1], 90, 70)
    jump_up_rect   = (start_location[0], start_location[1], 52, 59)
    jump_down_rect = (start_location[0], start_location[1], 52, 59)
    hurt_rect      = (start_location[0], start_location[1], 45, 60)

    # handle sound effects
    self.sound_attack = pg.mixer.Sound(attack_sound)
    self.sound_land = pg.mixer.Sound(land_sound)

    # handle the face image
    self.face_im = self.get_face_image(face_im, (180, 200))

    # handle walking frames
    self.rect = pg.Rect(rect)
    self.walk_frames = self.get_walk_frames(
        walk_im, [[i, 0] for i in xrange(6)], self.rect)

    # handle attacking frames
    self.attack_left_rect = pg.Rect(attack_rect)
    self.attack_right_rect = pg.Rect(attack_rect)
    self.attack_left_rect.x = self.rect.x - 28
    self.attack_right_rect.x = self.rect.x - 30
    self.attack_left_rect.y = self.rect.y - 10
    self.attack_right_rect.y = self.rect.y - 10
    self.attack_frames = self.get_attack_frames(
        attack_im, [[0,i] for i in xrange(4)], self.attack_right_rect)

    # handle jumping frames
    self.jump_up_rects, self.jump_down_rects = \
        self.get_jump_rects(jump_up_rect, jump_down_rect)
    self.jump_up_frames, self.jump_down_frames = self.get_jump_frames(
        jump_up_im, [[0,0]], pg.Rect(jump_up_rect),
        jump_down_im, [[0,0]], pg.Rect(jump_down_rect))

    # handle hurt frames
    self.hurt_rect = pg.Rect(hurt_rect)
    self.hurt_frames = self.get_hurt_frames(hurt_im, [[0, 0]], self.hurt_rect)

    # initialize the first image
    self.adjust_images()

  # Helper method to load face images
  def get_face_image(self, face_im, size):
    sheet = pg.image.load(face_im).convert()
    sheet.set_colorkey(player.Player.COLOR_KEY)
    sheet.set_alpha(150)
    frames = player.get_images(sheet, [[0, 0]], size)
    return frames[0]

  # Helper method to load walk frames
  def get_walk_frames(self, walk_im, indices, rect):
    sheet = pg.image.load(walk_im).convert()
    sheet.set_colorkey(player.Player.COLOR_KEY)
    frames = player.get_images(sheet, indices, rect.size)
    frame_dict = {self.LEFT_KEY : [frames[i] for i in xrange(6)],
                  self.RIGHT_KEY: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(6)]}
    return frame_dict

  # Helper method to get jump bounding boxes
  def get_jump_rects(self, jump_up_rect, jump_down_rect):
    jump_up_left_rect = pg.Rect(jump_up_rect)
    jump_up_right_rect = pg.Rect(jump_up_rect)
    jump_down_left_rect = pg.Rect(jump_down_rect)
    jump_down_right_rect = pg.Rect(jump_down_rect)

    jump_up_right_rect.x = self.rect.x - 18
    jump_down_right_rect.x = self.rect.x - 18

    jump_up_rects = {
      self.LEFT_KEY: jump_up_left_rect,
      self.RIGHT_KEY: jump_up_right_rect
    }
    jump_down_rects = {
      self.LEFT_KEY: jump_down_left_rect,
      self.RIGHT_KEY: jump_down_right_rect
    }
    return jump_up_rects, jump_down_rects


  # Helper method to load jump frames
  def get_jump_frames(self, jump1_im, indices1, rect1,
                            jump2_im, indices2, rect2):
    sheet1 = pg.image.load(jump1_im).convert()
    sheet1.set_colorkey(player.Player.COLOR_KEY)
    sheet2 = pg.image.load(jump2_im).convert()
    sheet2.set_colorkey(player.Player.COLOR_KEY)
    frames1 = player.get_images(sheet1, indices1, rect1.size)
    frames2 = player.get_images(sheet2, indices2, rect2.size)
    frame1_dict = {
      self.LEFT_KEY : [frames1[0]],
      self.RIGHT_KEY: [pg.transform.flip(frames1[0], True, False)]
    }
    frame2_dict = {
      self.LEFT_KEY : [pg.transform.flip(frames2[0], True, False)],
      self.RIGHT_KEY: [frames2[0]]
    }
    return frame1_dict, frame2_dict

  # Helper method to load attack frames
  def get_attack_frames(self, attack_im, indices, rect):
    sheet = pg.image.load(attack_im).convert()
    sheet.set_colorkey(player.Player.COLOR_KEY)
    frames = player.get_images(sheet, indices, rect.size)
    frame_dict = {self.LEFT_KEY : [frames[i] for i in xrange(4)],
                  self.RIGHT_KEY: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(4)]}
    return frame_dict

  # Helper method to load hurt frames
  def get_hurt_frames(self, hurt_im, indices, rect):
    sheet = pg.image.load(hurt_im).convert()
    sheet.set_colorkey(player.Player.COLOR_KEY)
    frames = player.get_images(sheet, indices, rect.size)
    frame_dict = {
      self.LEFT_KEY : [frames[0]],
      self.RIGHT_KEY: [pg.transform.flip(frames[0], True, False)]
    }
    return frame_dict

