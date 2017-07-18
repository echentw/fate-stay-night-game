import os
import pygame as pg

from src.scenes import single_player_menu as sp_menu
from src.scenes import single_player_game as sp_game
from src.scenes import two_player_menu as tp_menu
from src.scenes import two_player_game as tp_game
from src.scenes import main_menu
from src.scenes import two_player_game_over as tp_go
from src.scenes import single_player_game_over as sp_go

class State:
  MAIN_MENU               = 0
  SINGLE_PLAYER_MENU      = 1
  SINGLE_PLAYER_GAME      = 2
  SINGLE_PLAYER_GAME_OVER = 3
  TWO_PLAYER_MENU         = 4
  TWO_PLAYER_GAME         = 5
  TWO_PLAYER_GAME_OVER    = 6


class Control:
  CAPTION = "Fate/Stay Night Game"
  SCREEN_SIZE = (900, 700)

  def __init__(self):
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    pg.display.set_caption(Control.CAPTION)
    pg.display.set_mode(Control.SCREEN_SIZE)

    self.menu = main_menu.Menu(Control.SCREEN_SIZE)
    self.sp_menu = sp_menu.Menu(Control.SCREEN_SIZE)
    self.tp_menu = tp_menu.Menu(Control.SCREEN_SIZE)
    self.sp_game = sp_game.Game((1600, 700), self.sp_menu.player)
    self.tp_game = tp_game.Game((1600, 700), self.tp_menu.p1,
                                             self.tp_menu.p2)
    self.sp_go = sp_go.GameOver(Control.SCREEN_SIZE,
                                self.sp_game.win,
                                self.sp_menu.player)
    self.tp_go = tp_go.GameOver(Control.SCREEN_SIZE, self.tp_menu.p1)

    self.state = State.MAIN_MENU
    self.prev_state = None

    self.mute = False


  def start(self):
    while True:
      if self.state == State.MAIN_MENU:
        if self.prev_state != State.MAIN_MENU and \
           self.prev_state != State.SINGLE_PLAYER_MENU and \
           self.prev_state != State.TWO_PLAYER_MENU:
          pg.mixer.music.load("assets/music/kodoku-na-junrei.wav")
          pg.mixer.music.play()
        self.prev_state = self.state
        self.menu.reset()
        self.menu.main_loop()
        self.mute = self.menu.mute
        if self.menu.quit:
          return
        elif self.menu.state == main_menu.State.SINGLE_PLAYER:
          self.state = State.SINGLE_PLAYER_MENU
        elif self.menu.state == main_menu.State.TWO_PLAYER:
          self.state = State.TWO_PLAYER_MENU
        elif self.menu.state == main_menu.State.EXIT:
          return

      elif self.state == State.SINGLE_PLAYER_MENU:
        self.prev_state = self.state
        self.sp_menu.reset(self.mute)
        self.sp_menu.main_loop()
        if self.sp_menu.quit:
          return
        elif self.sp_menu.state == sp_menu.State.PLAY:
          self.state = State.SINGLE_PLAYER_GAME
        elif self.sp_menu.state == sp_menu.State.BACK:
          self.state = State.MAIN_MENU

      elif self.state == State.SINGLE_PLAYER_GAME:
        pg.mixer.music.load("assets/music/oath-sign-orchestra.wav")
        pg.mixer.music.play()
        self.prev_state = self.state
        self.sp_game.reset(self.sp_menu.player, self.mute)
        self.sp_game.main_loop()
        if self.sp_game.quit:
          return
        self.state = State.SINGLE_PLAYER_GAME_OVER

      elif self.state == State.TWO_PLAYER_MENU:
        self.prev_state = self.state
        self.tp_menu.reset(self.mute)
        self.tp_menu.main_loop()
        if self.tp_menu.quit:
          return
        elif self.tp_menu.state == tp_menu.State.PLAY:
          self.state = State.TWO_PLAYER_GAME
        elif self.tp_menu.state == tp_menu.State.BACK:
          self.state = State.MAIN_MENU

      elif self.state == State.TWO_PLAYER_GAME:
        pg.mixer.music.load("assets/music/oath-sign-orchestra.wav")
        pg.mixer.music.play()
        self.prev_state = self.state
        self.tp_game.reset(self.tp_menu.p1, self.tp_menu.p2, self.mute)
        self.tp_game.main_loop()
        if self.tp_game.quit:
          return
        self.state = State.TWO_PLAYER_GAME_OVER

      elif self.state == State.SINGLE_PLAYER_GAME_OVER:
        self.prev_state = self.state
        self.sp_go.reset(self.sp_game.win, self.sp_game.player, self.mute)
        self.sp_go.main_loop()
        if self.sp_go.quit:
          return
        elif self.sp_go.state == sp_go.State.MAIN_MENU:
          self.state = State.MAIN_MENU
        elif self.sp_go.state == sp_go.State.EXIT:
          return

      elif self.state == State.TWO_PLAYER_GAME_OVER:
        self.prev_state = self.state
        self.tp_go.reset(self.tp_game.winner, self.mute)
        self.tp_go.main_loop()
        if self.tp_go.quit:
          return
        elif self.tp_go.state == tp_go.State.MAIN_MENU:
          self.state = State.MAIN_MENU
        elif self.tp_go.state == tp_go.State.EXIT:
          return

