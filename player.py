import os
import sys
import pygame as pg

import control as ctrl


class Player(object):
    DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
                   pg.K_RIGHT : ( 1, 0),
                   pg.K_UP    : ( 0,-1),
                   pg.K_DOWN  : ( 0, 1)}
    COLOR_KEY = (255, 0, 255)

    """This class will represent our user controlled character."""
    def __init__(self, image_path, rect, speed, image2_path, rect2):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        self.rect = pg.Rect(rect)
        self.speed = speed
        self.direction = pg.K_RIGHT
        self.old_direction = None  #The Players previous direction every frame.
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.redraw = False  #Force redraw if needed.
        self.image = None
        self.frame = 0

        self.frames = self.get_frames(image_path, \
                                      [[i, 1] for i in xrange(6)], \
                                      self.rect.size)

        self.rect2 = pg.Rect(rect2);
        self.slashframes = []
        self.frames2 = self.get_frames(image2_path, \
                                       [[0,0]], \
                                       self.rect2.size)
        self.is_slash = False

        self.animate_timer = 0.0
        self.animate_fps = 7.0
        self.walkframes = []
        self.walkframe_dict = self.make_frame_dict()
        self.adjust_images()


    def get_frames(self, image_path, indices, size):
        """Get a list of all frames."""
        sheet = pg.image.load(image_path).convert()
        sheet.set_colorkey(Player.COLOR_KEY)
        return get_images(sheet, indices, size)

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet we need.
        """
        frames = {pg.K_LEFT : [self.frames[i] for i in xrange(6)],
                  pg.K_RIGHT: [pg.transform.flip(self.frames[i], True, False) \
                      for i in xrange(6)],
                  pg.K_DOWN : [self.frames[2]],
                  pg.K_UP   : [self.frames[2]],
                  pg.K_e: [self.frames2[0]]}
        return frames

    def adjust_images(self):
        """Update the sprites walkframes as the sprite's direction changes."""
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image()

    def make_image(self):
        """Update the sprite's animation as needed."""
        now = pg.time.get_ticks()
        if self.redraw or now-self.animate_timer > 1000/self.animate_fps:
            if self.is_slash:
                self.image = self.frames2[0]
            elif self.direction_stack:
                self.frame = (self.frame+1)%len(self.walkframes)
                self.image = self.walkframes[self.frame]
            else:
                self.image = self.walkframes[self.frame]
            self.animate_timer = now
        if not self.image:
            self.image = self.walkframes[self.frame]
        self.redraw = False

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in Player.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in Player.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def add_slash(self, key):
        if key == pg.K_e:
            self.is_slash = True

    def pop_slash(self, key):
        if key == pg.K_e:
            self.is_slash = False

    def update(self, screen_rect):
        """Updates our player appropriately every frame."""
        self.adjust_images()
        if self.direction_stack:
            direction_vector = Player.DIRECT_DICT[self.direction]
            self.rect.x += self.speed*direction_vector[0]
            self.rect.y += self.speed*direction_vector[1]
            self.rect.clamp_ip(screen_rect)

    def draw(self, surface):
        """Draws the player to the target surface."""
        surface.blit(self.image, self.rect)


def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0],size[1]*cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames

