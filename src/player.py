import os
import sys
import pygame as pg

import control as ctrl
import physics


class Player(physics.Physics, pg.sprite.Sprite):
  COLOR_KEY = (255, 0, 255)

  def __init__(self, keys):
    physics.Physics.__init__(self)
    pg.sprite.Sprite.__init__(self)

    self.name = ''                    # name (default value)
    self.health = 5                   # health (default value)
    self.jump_power = 12.0            # jumping power (default value)
    self.max_speed = 3                # max moving speed (default value)
    self.agility = 1                  # how quickly the player can change dir
    self.curr_frames = []             # the current set of frames to flip thru
    self.image = None                 # the current image of Player to display

    # handle the face image (beside the health bar)
    self.face_im = None

    # handle when to update the frames
    self.redraw = False
    self.animate_timer = 0.0
    self.animate_fps = 10.0

    # handle directions
    self.UP_KEY    = keys[0]
    self.DOWN_KEY  = keys[1]
    self.LEFT_KEY  = keys[2]
    self.RIGHT_KEY = keys[3]
    self.direct_dict = {self.LEFT_KEY : (-1, 0),
                        self.RIGHT_KEY: ( 1, 0)}
    self.direction = self.RIGHT_KEY       # the direction Player is facing
    self.old_direction = None             # the previous direction
    self.direction_stack = []

    # handle which frame to display
    self.frame_id = 0

    # handle walking frames
    self.rect = None
    self.walk_frames = None

    # handle attacking frames
    self.attack_left_rect = None
    self.attack_right_rect = None
    self.attack_frames = None
    self.attacking = False
    self.old_attacking = False
    self.attack_counter = 0

    # handle jumping frames
    self.jump_up_rects, self.jump_down_rects = None, None
    self.jump_up_frames, self.jump_down_frames = None, None

    # handle hurt frames
    self.hurt_rect = None
    self.hurt_frames = None
    self.hurt = False
    self.hurt_counter = 0

    # handle sound effects
    self.sound_attack = None
    self.sound_land = None

  # Handle getting hit
  def receive_attack(self, direction, attack_rect):
    if pg.Rect.colliderect(self.rect, attack_rect):
      self.health -= 1
      self.hurt = True
      self.hurt_counter = 20
      if direction == self.RIGHT_KEY:
        self.x_vel = -10
      elif direction == self.LEFT_KEY:
        self.x_vel = 10
      return True
    return False

  # Calculate Player's position in this frame
  def get_position(self, obstacles):
    self.check_falling(obstacles)
    self.physics_update()
    if self.y_vel:
      self.check_collisions(self.y_vel, 1, obstacles)
    if self.x_vel:
      self.check_collisions(self.x_vel, 0, obstacles)

  # Check if Player is making contact with something below
  def check_falling(self, obstacles):
    self.rect.move_ip((0, 1))
    is_collide_below = pg.sprite.spritecollide(self, obstacles, False)
    self.rect.move_ip((0, -1))
    if is_collide_below:
      self.y_vel = min(self.y_vel, 0)
      if self.y_vel == 0:
        if self.fall:
          self.sound_land.play()
        self.fall = False
    else:
      self.fall = True

  # Move up until a collision would happen
  def check_collisions(self, velocity, dir_id, obstacles):
    unaltered = True
    self.move_rects(dir_id, velocity)
    while pg.sprite.spritecollideany(self, obstacles):
      if velocity < 0:
        self.move_rects(dir_id, 1)
        if dir_id == 1:
          self.y_vel = 0
      else:
        self.move_rects(dir_id, -1)
      unaltered = False
    return unaltered

  # Helper method for self.check_collisions()
  def move_rects(self, dir_id, displacement):
    self.rect[dir_id] += displacement
    self.attack_left_rect[dir_id] += displacement
    self.attack_right_rect[dir_id] += displacement
    self.jump_up_rects[self.LEFT_KEY][dir_id] += displacement
    self.jump_up_rects[self.RIGHT_KEY][dir_id] += displacement
    self.jump_down_rects[self.LEFT_KEY][dir_id] += displacement
    self.jump_down_rects[self.RIGHT_KEY][dir_id] += displacement
    self.hurt_rect[dir_id] += displacement

  # Handle keypresses
  def handle_keydown(self, key, obstacles):
    if key in self.direct_dict:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      self.direction_stack.append(key)
      self.direction = key
    elif key == self.DOWN_KEY:
      if not self.fall and not self.attacking:
        self.attacking = True
        self.sound_attack.play()
    elif key == self.UP_KEY:
      if not self.fall:
        self.y_vel = -self.jump_power
        self.fall = True

  # Handle key releases
  def handle_keyup(self, key):
    if key in self.direct_dict:
      if key in self.direction_stack:
        self.direction_stack.remove(key)
      if self.direction_stack:
        self.direction = self.direction_stack[-1]

  # Update the image and position
  def update(self, screen_rect, obstacles):
    self.adjust_images()
    if self.direction_stack:
      direction_vector = self.direct_dict[self.direction]
      if self.direction == self.LEFT_KEY:
        self.x_vel -= self.agility
      elif self.direction == self.RIGHT_KEY:
        self.x_vel += self.agility
      if abs(self.x_vel) > self.max_speed:
        self.x_vel -= cmp(self.x_vel, 0) * self.agility
    self.get_position(obstacles)

  # Draw the image to the screen
  def draw(self, surface):
    if self.hurt:
      surface.blit(self.image, self.hurt_rect)
      return

    if self.old_attacking:
      if self.direction == self.LEFT_KEY:
        surface.blit(self.image, self.attack_left_rect)
      else:
        surface.blit(self.image, self.attack_right_rect)
    elif self.old_fall:
      if self.y_vel > 0:
        surface.blit(self.image, self.jump_up_rects[self.direction])
      else:
        surface.blit(self.image, self.jump_down_rects[self.direction])
    else:
      surface.blit(self.image, self.rect)

  # Helper method for update()
  def adjust_images(self):
    if self.old_direction is None:
      self.curr_frames = self.walk_frames[self.direction]
      self.old_direction = self.direction
      self.redraw = True

    # set the current frames
    # states: direction, falling, attacking
    if self.hurt:
      self.hurt_counter -= 1
      if self.hurt_counter < 1:
        self.hurt = False
        self.curr_frames = self.walk_frames[self.direction]
      else:
        self.curr_frames = self.hurt_frames[self.direction]
      self.redraw = True
    elif self.fall != self.old_fall:
      self.old_fall = self.fall
      self.redraw = True
      self.frame_id = -1
      if self.fall:
        if self.y_vel > 0:
          self.curr_frames = self.jump_down_frames[self.direction]
        else:
          self.curr_frames = self.jump_up_frames[self.direction]
      else:
        self.curr_frames = self.walk_frames[self.direction]
      self.attacking = False
      self.old_attacking = False
      self.attack_counter = 0
    elif self.attacking != self.old_attacking:
      self.old_attacking = self.attacking
      self.redraw = True
      self.frame_id = -1
      if self.attacking:
        self.curr_frames = self.attack_frames[self.direction]
      else:
        self.curr_frames = self.walk_frames[self.direction]
    elif self.direction != self.old_direction:
      self.old_direction = self.direction
      self.redraw = True
      self.frame_id = -1
      if self.attacking:
        self.curr_frames = self.attack_frames[self.direction]
      elif self.fall:
        if self.y_vel > 0:
          self.curr_frames = self.jump_down_frames[self.direction]
        else:
          self.curr_frames = self.jump_up_frames[self.direction]
      else:
        self.curr_frames = self.walk_frames[self.direction]
    elif self.fall:
      if self.old_y_vel <= 0 and self.y_vel > 0:
        self.redraw = True
        self.frame_id = -1
        self.curr_frames = self.jump_down_frames[self.direction]

    # set the frame id
    now = pg.time.get_ticks()
    if self.redraw or now - self.animate_timer > 1000 / self.animate_fps:
      if self.direction_stack or self.attacking or self.fall or self.hurt:
        self.frame_id = (self.frame_id + 1) % len(self.curr_frames)
      if self.attacking:
        self.attack_counter += 1
        if self.attack_counter == len(self.attack_frames[self.direction]):
          self.attacking = False
          self.attack_counter = 0
      self.image = self.curr_frames[self.frame_id]
      self.animate_timer = now
      self.redraw = False

  # Helper method to load walk frames
  def get_walk_frames(self, walk_im, indices, rect):
    pass

  # Helper method to get jump bounding boxes
  def get_jump_rects(self, jump_up_rect, jump_down_rect):
    pass

  # Helper method to load jump frames
  def get_jump_frames(self, jump_up_im, indices1, rect1,
                            jump_down_im, indices2, rect2):
    pass

  # Helper method to load attack frames
  def get_attack_frames(self, attack_im, indices, rect):
    pass


# Helper method
def get_images(sheet, frame_indices, size):
  frames = []
  for cell in frame_indices:
    frame_rect = ((size[0] * cell[0], size[1] * cell[1]), size)
    frames.append(sheet.subsurface(frame_rect))
  return frames

