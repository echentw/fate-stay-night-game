import os
import sys
import pygame as pg

import player as myplayer

class Control(object):
    CAPTION = "My Game"
    BACKGROUND_COLOR = (100, 100, 100)

    """Being controlling is our job."""
    def __init__(self):
        """Initialize standard attributes, standardly."""
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock  = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = myplayer.Player("saber_walk.png", (0,0,38,54), 3, \
                                      "saber_slash.png", (0,0,73,48))

        self.player.rect.center = self.screen_rect.center
        self.player.rect2.x = self.player.rect.x - 40
        self.player.rect2.y = self.player.rect.y
        self.player.rect3.x = self.player.rect.x + 10
        self.player.rect3.y = self.player.rect.y

    def event_loop(self):
        """Add/pop directions from player's direction stack as necessary."""
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.player.add_slash(event.key)
                else:
                    self.player.add_direction(event.key)
            elif event.type == pg.KEYUP:
                self.player.pop_direction(event.key)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        pg.display.set_caption(Control.CAPTION)

    def main_loop(self):
        """Our main game loop; I bet you'd never have guessed."""
        while not self.done:
            self.event_loop()
            self.player.update(self.screen_rect)
            self.screen.fill(Control.BACKGROUND_COLOR)
            self.player.draw(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

