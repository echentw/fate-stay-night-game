import os
import sys
import pygame as pg

import control as ctrl
import physics


class Saber(physics.Physics, pg.sprite.Sprite):
  DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
                 pg.K_RIGHT : ( 1, 0)}
  COLOR_KEY = (255, 0, 255)

  def __init__(self, walk_im, rect, slash_im, slash_rect, speed):
    physics.Physics.__init__(self)
    pg.sprite.Sprite.__init__(self)

    self.jump_power = -9.0            # initial jumping speed
    self.speed = speed                # the speed Saber moves at
    self.curr_frames = []             # the current set of frames to flip thru
    self.image = None                 # the current image of saber to display

    # handle when to update the frames
    self.redraw = False
    self.animate_timer = 0.0
    self.animate_fps = 10.0

    # handle the state of Saber
    self.slashing = False

    # handle directions
    self.direction = pg.K_RIGHT       # the direction Saber is facing
    self.old_direction = None         # the previous direction
    self.direction_stack = []

    # handle which frame to display
    self.frame_id = 0

    # handle walking frames
    self.rect = pg.Rect(rect)
    self.walk_frames = self.get_walk_frames(
        walk_im, [[i, 1] for i in xrange(6)], self.rect)

    # handle slashing frames
    self.slash_left_rect = pg.Rect(slash_rect)
    self.slash_right_rect = pg.Rect(slash_rect)
    self.slash_left_rect.x = self.rect.x - 36
    self.slash_frames = self.get_slash_frames(
        slash_im, [[0,0]], self.slash_right_rect)

    # initialize the first image
    self.adjust_images()

  # Calculate Saber's position in this frame
  def get_position(self, obstacles):
    self.check_falling(obstacles)
    self.physics_update()
    if self.y_vel:
      self.rect.y += self.y_vel
      self.slash_left_rect.y = self.rect.y
      self.slash_right_rect.y = self.rect.y
    if self.x_vel:
      self.rect.x += self.x_vel
      self.slash_left_rect.x = self.rect.x - 36
      self.slash_right_rect.x = self.rect.x
      self.x_vel = 0

  # Check if Saber is making contact with something below
  def check_falling(self, obstacles):
    self.rect.move_ip((0, 1))
    is_collide_below = pg.sprite.spritecollide(self, obstacles, False)
    self.rect.move_ip((0, -1))
    if is_collide_below:
      self.y_vel = min(self.y_vel, 0)
      if self.y_vel == 0:
        self.fall = False
    else:
      self.fall = True

  # Handle keypresses
  def handle_keydown(self, key, obstacles):
    if key in Saber.DIRECT_DICT:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      self.direction_stack.append(key)
      self.direction = key
    elif key == pg.K_e:
      self.slashing = True
    elif key == pg.K_UP:
      if not self.fall:
        self.y_vel = self.jump_power
        self.fall = True

  # Handle key releases
  def handle_keyup(self, key):
    if key in Saber.DIRECT_DICT:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      if self.direction_stack:
        self.direction = self.direction_stack[-1]

  # Update the image and position
  def update(self, screen_rect, obstacles):
    self.adjust_images()
    if self.direction_stack:
      direction_vector = Saber.DIRECT_DICT[self.direction]
      if self.direction == pg.K_LEFT:
        self.x_vel -= self.speed
      elif self.direction == pg.K_RIGHT:
        self.x_vel += self.speed
    self.get_position(obstacles)

  # Draw the image to the screen
  def draw(self, surface):
    if self.image == self.slash_frames[self.direction][0]:
      if self.direction == pg.K_LEFT:
        surface.blit(self.image, self.slash_left_rect)
      else:
        surface.blit(self.image, self.slash_right_rect)
      self.slashing = False
    else:
      surface.blit(self.image, self.rect)

  # Helper method for update()
  def adjust_images(self):
    if self.slashing:
      self.curr_frames = self.slash_frames[self.direction]
      self.redraw = True
    elif self.direction != self.old_direction:
      self.curr_frames = self.walk_frames[self.direction]
      self.old_direction = self.direction
      self.redraw = True
    now = pg.time.get_ticks()
    if self.redraw or now - self.animate_timer > 1000 / self.animate_fps:
      if self.direction_stack or self.slashing:
        self.frame_id = (self.frame_id + 1) % len(self.curr_frames)
      else:
        self.curr_frames = self.walk_frames[self.direction]
      self.image = self.curr_frames[self.frame_id]
      self.animate_timer = now
      self.redraw = False

  # Helper method to load walk frames
  def get_walk_frames(self, walk_im, indices, rect):
    sheet = pg.image.load(walk_im).convert()
    sheet.set_colorkey(Saber.COLOR_KEY)
    frames = get_images(sheet, indices, rect.size)
    frame_dict = {pg.K_LEFT : [frames[i] for i in xrange(6)],
                  pg.K_RIGHT: [pg.transform.flip(frames[i], True, False) \
                      for i in xrange(6)]}
    return frame_dict

  # Helper method to load slash frames
  def get_slash_frames(self, slash_im, indices, rect):
    sheet = pg.image.load(slash_im).convert()
    sheet.set_colorkey(Saber.COLOR_KEY)
    frames = get_images(sheet, indices, rect.size)
    frame_dict = {pg.K_LEFT : [frames[0]],
                  pg.K_RIGHT: [pg.transform.flip(frames[0], True, False)]}
    return frame_dict


# Helper method
def get_images(sheet, frame_indices, size):
  frames = []
  for cell in frame_indices:
    frame_rect = ((size[0] * cell[0], size[1] * cell[1]), size)
    frames.append(sheet.subsurface(frame_rect))
  return frames

