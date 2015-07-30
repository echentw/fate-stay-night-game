import os
import sys
import pygame as pg

import saber as sab

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
        self.saber = sab.Saber("saber_walk.png", (0,0,38,54),
                                    "saber_slash.png", (0,0,73,48), 3)

        self.saber.walk_rect.center = self.screen_rect.center

    def event_loop(self):
        """Add/pop directions from player's direction stack as necessary."""
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.saber.handle_keydown(event.key)
            elif event.type == pg.KEYUP:
                self.saber.handle_keyup(event.key)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        pg.display.set_caption(Control.CAPTION)

    def main_loop(self):
        """Our main game loop; I bet you'd never have guessed."""
        while not self.done:
            self.event_loop()
            self.saber.update(self.screen_rect)
            self.screen.fill(Control.BACKGROUND_COLOR)
            self.saber.draw(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

