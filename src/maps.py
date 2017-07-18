import pygame as pg

import src.obstacles as ob

SIZE = 20

def get_original_map():
  walls = [ob.Brick((0 * SIZE, 48 * SIZE, 50 * SIZE, 2 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 50 * SIZE, 2 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 3 * SIZE, 50 * SIZE)),
           ob.Brick((47 * SIZE, 0 * SIZE, 3 * SIZE, 50 * SIZE))]

  ground = [ob.Brick((1 * SIZE, 42 * SIZE, 32 * SIZE, 6 * SIZE)),
            ob.Brick((1 * SIZE, 36 * SIZE, 17 * SIZE, 6 * SIZE))]

  big = [ob.Brick((5 * SIZE, 18 * SIZE, 9 * SIZE, 13 * SIZE)),
         ob.Brick((4 * SIZE, 23 * SIZE, 1 * SIZE, 1 * SIZE)),
         ob.Brick((4 * SIZE, 30 * SIZE, 1 * SIZE, 1 * SIZE)),
         ob.Brick((14 * SIZE, 23 * SIZE, 1 * SIZE, 1 * SIZE)),
         ob.Brick((14 * SIZE, 30 * SIZE, 1 * SIZE, 1 * SIZE))]

  floating = [ob.Brick((20 * SIZE, 21 * SIZE, 9 * SIZE, 2 * SIZE)),
              ob.Brick((23 * SIZE, 31 * SIZE, 15 * SIZE, 1 * SIZE)),
              ob.Brick((33 * SIZE, 19 * SIZE, 1 * SIZE, 1 * SIZE)),
              ob.Brick((37 * SIZE, 16 * SIZE, 7 * SIZE, 2 * SIZE))]

  high = [ob.Brick((6 * SIZE, 9 * SIZE, 3 * SIZE, 2 * SIZE)),
          ob.Brick((15 * SIZE, 9 * SIZE, 3 * SIZE, 2 * SIZE)),
          ob.Brick((24 * SIZE, 9 * SIZE, 3 * SIZE, 2 * SIZE)),
          ob.Brick((33 * SIZE, 9 * SIZE, 3 * SIZE, 2 * SIZE))]

  high_pillars = [ob.Pillar((6 * SIZE, 8 * SIZE, 3 * SIZE, 1 * SIZE)),
                  ob.Pillar((15 * SIZE, 8 * SIZE, 3 * SIZE, 1 * SIZE)),
                  ob.Pillar((24 * SIZE, 8 * SIZE, 3 * SIZE, 1 * SIZE)),
                  ob.Pillar((33 * SIZE, 8 * SIZE, 3 * SIZE, 1 * SIZE))]

  floating_pillars = [ob.Pillar((20 * SIZE, 20 * SIZE, 9 * SIZE, 1 * SIZE)),
                      ob.Pillar((23 * SIZE, 30 * SIZE, 15 * SIZE, 1 * SIZE)),
                      ob.Pillar((37 * SIZE, 15 * SIZE, 7 * SIZE, 1 * SIZE))]
  return (pg.sprite.Group(walls, ground, big, floating, high),
          pg.sprite.Group(high_pillars, floating_pillars))

def get_simple_map():
  walls = [ob.Brick((0 * SIZE, 33 * SIZE, 80 * SIZE, 2 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 80 * SIZE, 2 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 3 * SIZE, 35 * SIZE)),
           ob.Brick((78 * SIZE, 0 * SIZE, 3 * SIZE, 35 * SIZE))]

  floating = [ob.Brick((20 * SIZE, 28 * SIZE, 10 * SIZE, 1 * SIZE))]

  return (pg.sprite.Group(walls, floating),
          pg.sprite.Group())

def get_complex_map():
  walls = [ob.Brick((0 * SIZE, 32 * SIZE, 80 * SIZE, 3 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 80 * SIZE, 3 * SIZE)),
           ob.Brick((0 * SIZE, 0 * SIZE, 3 * SIZE, 35 * SIZE)),
           ob.Brick((77 * SIZE, 0 * SIZE, 3 * SIZE, 35 * SIZE))]

  part1 = [ob.Brick((3 * SIZE, 27 * SIZE, 2 * SIZE, 1 * SIZE)),
           ob.Brick((19 * SIZE, 27 * SIZE, 9 * SIZE, 1 * SIZE)),
           ob.Brick((14 * SIZE, 23 * SIZE, 4 * SIZE, 1 * SIZE)),
           ob.Brick((3 * SIZE, 19 * SIZE, 10 * SIZE, 1 * SIZE)),
           ob.Brick((3 * SIZE, 14 * SIZE, 1 * SIZE, 1 * SIZE)),
           ob.Brick((9 * SIZE, 10 * SIZE, 22 * SIZE, 1 * SIZE))]

  part2 = [ob.Brick((36 * SIZE, 14 * SIZE, 5 * SIZE, 18 * SIZE)),
           ob.Brick((41 * SIZE, 14 * SIZE, 5 * SIZE, 1 * SIZE)),
           ob.Brick((53 * SIZE, 3 * SIZE, 4 * SIZE, 22 * SIZE)),
           ob.Brick((45 * SIZE, 24 * SIZE, 8 * SIZE, 1 * SIZE))]

  part3 = [ob.Brick((62 * SIZE, 26 * SIZE, 4 * SIZE, 1 * SIZE)),
           ob.Brick((71 * SIZE, 21 * SIZE, 6 * SIZE, 1 * SIZE)),
           ob.Brick((60 * SIZE, 18 * SIZE, 6 * SIZE, 1 * SIZE)),
           ob.Brick((71 * SIZE, 13 * SIZE, 6 * SIZE, 1 * SIZE)),
           ob.Brick((57 * SIZE, 10 * SIZE, 9 * SIZE, 1 * SIZE))]

  pillars = [ob.Pillar((9 * SIZE, 9 * SIZE, 22 * SIZE, 1 * SIZE)),
             ob.Pillar((36 * SIZE, 13 * SIZE, 10 * SIZE, 1 * SIZE))]

  return (pg.sprite.Group(walls, part1, part2, part3),
          pg.sprite.Group(pillars))
