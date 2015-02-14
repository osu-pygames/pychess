from __future__ import print_function
# in python 3.x range is removed and xrange is renamed  to range
range = xrange

import sys
import os
import time

from board import Board

import pygame
import pygame.locals


class Color(object):
    """
    A container object for color definitions
    """
    # "name"       r    g    b
    RED       = (215, 000, 000)
    BLUE      = (000, 000, 220)
    GREEN     = (000, 185, 000)
    BLACK     = (000, 000, 000)


class Config(object):
    sublime = True
    piece_size = 42     # chess piece square size
    piece_border = 8    # chess piece border size
    box_size = piece_size + piece_border
    tick_rate = 0.1


def init_pygame():
    """
    Handles pygame initialization and ensuring the game settings will work
    with the player's monitor resolution.
    """
    pygame.init()

    # get the user's current screen resolution
    screen_info = pygame.display.Info()
    screen_x = screen_info.current_w
    screen_y = screen_info.current_h

    min_resolution = Config.box_size * 8

    if (screen_x == -1 or screen_y == -1):
        print("display info error, or your version of pygame is too old")
        stop_game()

    if (screen_x < min_resolution) \
    or (screen_y < min_resolution):
        print("The board settings are too large for your monitor")
        print("You would need a %dp," % min_resolution,
              "or greater, resolution to play at these settings.")
        print("Lower the game settings or raise your desktop resolution.")
        stop_game()

    return min_resolution

"""
board.move(start, finish)
    "invalid"
    "success"
board.iterpieces()
    give x,y coordinate
    give type of piece
    give color
"""

# tell pygame to center the game window location
# on your screen when it gets created.
os.environ['SDL_VIDEO_CENTERED'] = "1"

class Pychess(object):
    def __init__(self):
        if Config.sublime:
            self.host = "h"
        else: # sublime text does not support raw_input
            self.host = raw_input("Host or client?")
        self.host = self.host[0]
        self.host = self.host.lower()
        if self.host == "h":
            self.host = True
            print("You are a host")
        elif self.host:
            self.host = False
            print("You are a client")
        else:
            print("I don't know what you are")
            stop_game()

        min_resolution = init_pygame()
        self.window = pygame.display
        self.screen = self.window.set_mode((min_resolution, min_resolution))
        self.window.set_caption("pysnake")

        self.board = Board()

    def start(self):
        self.turn = "black"
        while True:
            self.game_tick()
            time.sleep(Config.tick_rate)

    def game_tick(self):
        self.get_input()
        self.draw_screen()

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                stop_game()
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    stop_game()

    def draw_screen(self):
        self.draw_background()
        self.draw_board()
        self.window.update()

    def draw_background(self):
        size = Config.box_size
        self.screen.fill(Color.BLACK)
        for row in range(8):
            if row % 2 == 0:
                for col in range(8):
                    if col % 2 == 0:
                        rect = pygame.Rect((row*size, col*size), (size,size))
                        pygame.draw.rect(self.screen, Color.GREEN, rect)

        for row in range(0, 8):
            if row % 2 == 1:
                for col in range(0, 8):
                    if col % 2 == 1:
                        rect = pygame.Rect((row*size, col*size), (size,size))
                        pygame.draw.rect(self.screen, Color.GREEN, rect)

    def update_tick(self):
        pass

    def draw_board(self):
        pass


def stop_game():
    pygame.quit()
    sys.exit()


def main():
    game = Pychess()
    game.start()


if __name__ == "__main__":
    main()
