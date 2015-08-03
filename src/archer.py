import os
import sys
import pygame as pg

import control as ctrl
import physics
import player


class Archer(player.Player):
  def __init__(self, speed, keys, walk_im, rect,
                                  slash_im, slash_rect,
                                  jump1_im, jump1_rect,
                                  jump2_im, jump2_rect):

    # sound files
    sound_swoosh_file = "assets/soundfx/knife_stab.wav"
    sound_land_file = "assets/soundfx/thud.wav"

    player.Player.__init__(self, speed, keys,
                                 walk_im, rect,
                                 slash_im, slash_rect,
                                 jump1_im, jump1_rect,
                                 jump2_im, jump2_rect,
                                 sound_swoosh_file, sound_land_file)

    # handle walking frames
    self.rect = pg.Rect(rect)
    self.walk_frames = self.get_walk_frames(
        walk_im, [[i, 0] for i in xrange(6)], self.rect)

    # handle jumping frames
    self.jump1_rect = pg.Rect(jump1_rect)
    self.jump2_rect = pg.Rect(jump2_rect)
    self.jump_frames1, self.jump_frames2 = self.get_jump_frames(
        jump1_im, [[0,0]], self.jump1_rect,
        jump2_im, [[0,0]], self.jump2_rect)

    # handle slashing frames
    self.slash_left_rect = pg.Rect(slash_rect)
    self.slash_right_rect = pg.Rect(slash_rect)
    self.slash_left_rect.x = self.rect.x - 28
    self.slash_right_rect.x = self.rect.x - 30
    self.slash_left_rect.y = self.rect.y - 10
    self.slash_right_rect.y = self.rect.y - 10
    self.slash_frames = self.get_slash_frames(
        slash_im, [[0,i] for i in xrange(4)], self.slash_right_rect)

    # initialize the first image
    self.adjust_images()


  # Helper method to load walk frames
  def get_walk_frames(self, walk_im, indices, rect):
    sheet = pg.image.load(walk_im).convert()
    sheet.set_colorkey(Archer.COLOR_KEY)
    frames = get_images(sheet, indices, rect.size)
    frame_dict = {self.LEFT_KEY : [frames[i] for i in xrange(6)],
                  self.RIGHT_KEY: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(6)]}
    return frame_dict

  # Helper method to load jump frames
  def get_jump_frames(self, jump1_im, indices1, rect1,
                            jump2_im, indices2, rect2):
    sheet1 = pg.image.load(jump1_im).convert()
    sheet1.set_colorkey(Archer.COLOR_KEY)
    sheet2 = pg.image.load(jump2_im).convert()
    sheet2.set_colorkey(Archer.COLOR_KEY)
    frames1 = get_images(sheet1, indices1, rect1.size)
    frames2 = get_images(sheet2, indices2, rect2.size)
    frame1_dict = {
      self.LEFT_KEY : [frames1[0]],
      self.RIGHT_KEY: [pg.transform.flip(frames1[0], True, False)]
    }
    frame2_dict = {
      self.LEFT_KEY : [pg.transform.flip(frames2[0], True, False)],
      self.RIGHT_KEY: [frames2[0]]
    }
    return frame1_dict, frame2_dict

  # Helper method to load slash frames
  def get_slash_frames(self, slash_im, indices, rect):
    sheet = pg.image.load(slash_im).convert()
    sheet.set_colorkey(Archer.COLOR_KEY)
    frames = get_images(sheet, indices, rect.size)
    frame_dict = {self.LEFT_KEY : [frames[i] for i in xrange(4)],
                  self.RIGHT_KEY: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(4)]}
    return frame_dict


# Helper method
def get_images(sheet, frame_indices, size):
  frames = []
  for cell in frame_indices:
    frame_rect = ((size[0] * cell[0], size[1] * cell[1]), size)
    frames.append(sheet.subsurface(frame_rect))
  return frames

