import os
import pygame as pg

from scenes import single_player_menu as sp_menu
from scenes import single_player_game as sp_game
from scenes import two_player_menu as tp_menu
from scenes import two_player_game as tp_game
from scenes import main_menu
from scenes import game_over

class State:
  MAIN_MENU = 0
  SINGLE_PLAYER_MENU = 1
  SINGLE_PLAYER_GAME = 3
  TWO_PLAYER_MENU = 2
  TWO_PLAYER_GAME = 4
  TWO_PLAYER_GAME_OVER = 5


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
    self.sp_game = sp_game.Game((1000, 1000), self.sp_menu.player)
    self.tp_game = tp_game.Game((1000, 1000), self.tp_menu.player1,
                                              self.tp_menu.player2)
    self.game_over = game_over.GameOver(Control.SCREEN_SIZE)

    self.state = State.MAIN_MENU
    self.prev_state = None


  def start(self):
    while True:
      if self.state == State.MAIN_MENU:
        pg.mixer.music.load("assets/music/kodoku-na-junrei.wav")
        pg.mixer.music.play()

        self.menu.reset()
        self.menu.main_loop()
        if self.menu.state == main_menu.State.SINGLE_PLAYER:
          self.state = State.SINGLE_PLAYER_MENU
        elif self.menu.state == main_menu.State.TWO_PLAYER:
          self.state = State.TWO_PLAYER_MENU
        elif self.menu.state == main_menu.State.EXIT:
          return

      elif self.state == State.SINGLE_PLAYER_MENU:
        self.sp_menu.reset()
        self.sp_menu.main_loop()
        if self.sp_menu.state == sp_menu.State.PLAY:
          self.state = State.SINGLE_PLAYER_GAME
        elif self.sp_menu.state == sp_menu.State.BACK:
          self.state = State.MAIN_MENU

      elif self.state == State.SINGLE_PLAYER_GAME:
        self.sp_game.reset(self.sp_menu.player)
        self.sp_game.main_loop()
        if self.sp_game.quit:
          return
        print 'not implemented!'
        return

      elif self.state == State.TWO_PLAYER_MENU:
        self.tp_menu.reset()
        self.tp_menu.main_loop()
        if self.tp_menu.state == tp_menu.State.PLAY:
          self.state = State.TWO_PLAYER_GAME
        elif self.tp_menu.state == tp_menu.State.BACK:
          self.state = State.MAIN_MENU

      elif self.state == State.TWO_PLAYER_GAME:
        self.tp_game.reset(self.tp_menu.player1, self.tp_menu.player2)
        self.tp_game.main_loop()
        if self.tp_game.quit:
          return
        self.state = State.TWO_PLAYER_GAME_OVER

      elif self.state == State.TWO_PLAYER_GAME_OVER:
        self.game_over.reset()
        self.game_over.set_winner(self.tp_game.winner)
        self.game_over.main_loop()
        if self.game_over.state == game_over.State.MAIN_MENU:
          self.state = State.MAIN_MENU
        elif self.game_over.state == game_over.State.EXIT:
          return

