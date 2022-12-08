import random
from math import radians, cos, sin
import Paddle

class Ball:
    def __init__(self, color, rightPaddle: Paddle, leftPaddle: Paddle, win_width, win_height, margin, pygame, display):
        self.r = 20
        self.x = win_width/2 - self.r/2
        self.y = win_height/2 -self.r/2
        self.color = color
        self.angle = random.randint(-75, 75)
        if random.randint(0, 1):
            self.angle += 180
        
        self.win_height = win_height
        self.win_width = win_width
        self.margin = margin

        self.speed = 4

        self.pygame = pygame
        self.display = display
        self.rightPaddle = rightPaddle
        self.leftPaddle = leftPaddle

        self.scoreLeft = 0
        self.scoreRight = 0

  
    def show(self):
        self.pygame.draw.ellipse(self.display, self.color, (self.x, self.y, self.r, self.r))


    def setPos(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.speed*cos(radians(self.angle))
        self.y += self.speed*sin(radians(self.angle))
        if self.x + self.r > self.win_width - self.margin:
            self.scoreLeft += 1
            self.angle = 180 - self.angle
        if self.x < self.margin:
            self.scoreRight += 1
            self.angle = 180 - self.angle
        if self.y < self.margin:
            self.angle = - self.angle
        if self.y + self.r  >= self.win_height - self.margin:
            self.angle = - self.angle
        return self.scoreLeft, self.scoreRight

   
    def checkForPaddle(self):
        if self.x < self.win_width/2:
            if self.leftPaddle.x < self.x < self.leftPaddle.x + self.leftPaddle.w:
                if self.leftPaddle.y < self.y < self.leftPaddle.y + 10 or self.leftPaddle.y < self.y + self.r< self.leftPaddle.y + 10:
                    self.angle = -45
                if self.leftPaddle.y + 10 < self.y < self.leftPaddle.y + 20 or self.leftPaddle.y + 10 < self.y + self.r< self.leftPaddle.y + 20:
                    self.angle = -30
                if self.leftPaddle.y + 20 < self.y < self.leftPaddle.y + 30 or self.leftPaddle.y + 20 < self.y + self.r< self.leftPaddle.y + 30:
                    self.angle = -15
                if self.leftPaddle.y + 30 < self.y < self.leftPaddle.y + 40 or self.leftPaddle.y + 30 < self.y + self.r< self.leftPaddle.y + 40:
                    self.angle = -10
                if self.leftPaddle.y + 40 < self.y < self.leftPaddle.y + 50 or self.leftPaddle.y + 40 < self.y + self.r< self.leftPaddle.y + 50:
                    self.angle = 10
                if self.leftPaddle.y + 50 < self.y < self.leftPaddle.y + 60 or self.leftPaddle.y + 50 < self.y + self.r< self.leftPaddle.y + 60:
                    self.angle = 15
                if self.leftPaddle.y + 60 < self.y < self.leftPaddle.y + 70 or self.leftPaddle.y + 60 < self.y + self.r< self.leftPaddle.y + 70:
                    self.angle = 30
                if self.leftPaddle.y + 70 < self.y < self.leftPaddle.y + 80 or self.leftPaddle.y + 70 < self.y + self.r< self.leftPaddle.y + 80:
                    self.angle = 45
        else:
            if self.rightPaddle.x + self.rightPaddle.w > self.x  + self.r > self.rightPaddle.x:
                if self.rightPaddle.y < self.y < self.leftPaddle.y + 10 or self.leftPaddle.y < self.y + self.r< self.leftPaddle.y + 10:
                    self.angle = -135
                if self.rightPaddle.y + 10 < self.y < self.rightPaddle.y + 20 or self.rightPaddle.y + 10 < self.y + self.r< self.rightPaddle.y + 20:
                    self.angle = -150
                if self.rightPaddle.y + 20 < self.y < self.rightPaddle.y + 30 or self.rightPaddle.y + 20 < self.y + self.r< self.rightPaddle.y + 30:
                    self.angle = -165
                if self.rightPaddle.y + 30 < self.y < self.rightPaddle.y + 40 or self.rightPaddle.y + 30 < self.y + self.r< self.rightPaddle.y + 40:
                    self.angle = 170
                if self.rightPaddle.y + 40 < self.y < self.rightPaddle.y + 50 or self.rightPaddle.y + 40 < self.y + self.r< self.rightPaddle.y + 50:
                    self.angle = 190
                if self.rightPaddle.y + 50 < self.y < self.rightPaddle.y + 60 or self.rightPaddle.y + 50 < self.y + self.r< self.rightPaddle.y + 60:
                    self.angle = 165
                if self.rightPaddle.y + 60 < self.y < self.rightPaddle.y + 70 or self.rightPaddle.y + 60 < self.y + self.r< self.rightPaddle.y + 70:
                    self.angle = 150
                if self.rightPaddle.y + 70 < self.y < self.rightPaddle.y + 80 or self.rightPaddle.y + 70 < self.y + self.r< self.rightPaddle.y + 80:
                     self.angle = 135
