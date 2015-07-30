import os
import sys
import pygame as pg

import control as ctrl


class Saber(object):
  DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
                 pg.K_RIGHT : ( 1, 0)}
  COLOR_KEY = (255, 0, 255)

  def __init__(self, walk_im, walk_rect, slash_im, slash_rect, speed):
    self.speed = speed                # the speed Saber moves at
    self.curr_frames = []             # the current set of frames to flip thru
    self.image = None                 # the current image of saber to display

    # handle when to update the frames
    self.animate_timer = 0.0
    self.animate_fps = 10.0

    # handle directions
    self.direction = pg.K_RIGHT       # the direction Saber is facing
    self.old_direction = None         # the previous direction
    self.direction_stack = []

    # handle walking frames
    self.walk_rect = pg.Rect(walk_rect)
    self.walk_frames = self.get_walk_frames(
        walk_im, [[i, 1] for i in xrange(6)], self.walk_rect)
    self.walk_id = 0

    # handle slashing frames
#    self.slash_rect = pg.Rect(slash_rect)
#    self.slash_frames = self.get_slash_frames(
#        slash_im, [[0,0]], slash_rect)

    self.adjust_images()             # initialize the first image

  def handle_keydown(self, key):
    if key in Saber.DIRECT_DICT:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      self.direction_stack.append(key)
      self.direction = key

  def handle_keyup(self, key):
    if key in Saber.DIRECT_DICT:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      if self.direction_stack:
        self.direction = self.direction_stack[-1]

  # Update the image and position
  def update(self, screen_rect):
    self.adjust_images()
    if self.direction_stack:
      direction_vector = Saber.DIRECT_DICT[self.direction]
      self.walk_rect.x += self.speed * direction_vector[0]
      self.walk_rect.y += self.speed * direction_vector[1]
      self.walk_rect.clamp_ip(screen_rect)

  # Draw the image to the screen
  def draw(self, surface):
    surface.blit(self.image, self.walk_rect)

  def adjust_images(self):
    redraw = False
    if self.direction != self.old_direction:
      self.curr_frames = self.walk_frames[self.direction]
      self.old_direction = self.direction
      redraw = True
    now = pg.time.get_ticks()
    if redraw or now - self.animate_timer > 1000 / self.animate_fps:
      if self.direction_stack:
        self.walk_id = (self.walk_id + 1) % len(self.curr_frames)
      self.image = self.curr_frames[self.walk_id]
      self.animate_timer = now

  # Helper method
  def get_walk_frames(self, walk_im, indices, rect):
    sheet = pg.image.load(walk_im).convert()
    sheet.set_colorkey(Saber.COLOR_KEY)
    frames = get_images(sheet, indices, rect.size)
    frame_dict = {pg.K_LEFT : [frames[i] for i in xrange(6)],
                  pg.K_RIGHT: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(6)]}
    return frame_dict


# Helper method
def get_images(sheet, frame_indices, size):
  frames = []
  for cell in frame_indices:
    frame_rect = ((size[0] * cell[0], size[1] * cell[1]), size)
    frames.append(sheet.subsurface(frame_rect))
  return frames

