from Game import Game
from Ball import Ball
from Player import Player
from Paddle import Paddle
import pygame
from math import *

pygame.init()

win_width = 600
win_height = 400
display = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Pong the Game")
clock = pygame.time.Clock()

background = (27, 38, 49)
white = (236, 240, 241)
red = (203, 67, 53)
blue = (52, 152, 219)
yellow = (244, 208, 63)

top = white
bottom = white
left = white
right = white

margin = 4

font = pygame.font.SysFont("Small Fonts", 30)
largeFont = pygame.font.SysFont("Small Fonts", 60)


leftPaddle = Paddle(-1, win_width, win_height, margin, pygame, white, display)
rightPaddle = Paddle(1, win_width, win_height, margin, pygame, white, display)


p1 = Player(1, pygame.K_w, pygame.K_s)
# p2 = Player(2, pygame.K_UP, pygame.K_DOWN)


ball = Ball(yellow, rightPaddle, leftPaddle,
            win_width, win_height, margin, pygame, display)


leftScoreColor = red
rightScoreColor = blue

game = Game(ball, leftPaddle, rightPaddle, clock, pygame, background, white, left, right, top,
            bottom, display, font, largeFont, win_width, win_height, margin, leftScoreColor, rightScoreColor,)
game.init()


host = 'localhost'
port = 59885


from Server import Server
server = Server(port)

def serve():
    server.run()
    server.start_emittion(ball)


import threading


thread = threading.Thread(target=serve)
thread.daemon = True
thread.start()


from Client import Client 

import time

time.sleep(1)

client = Client(host, port, game)
client.listen()

game.setPlayer(p1, client.send)
game.start()
