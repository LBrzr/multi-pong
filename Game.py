from Ball import Ball
from Paddle import Paddle
from Player import Player

import json
import sys

class Game:
    
    def __init__(self, ball: Ball, leftPaddle: Paddle, rightPaddle: Paddle, clock, pygame, background, boundaryColor, left, right, top, bottom, display, font, largeFont, win_width, win_height, margin, leftScoreColor, rightScoreColor, maxScore=20,) -> None:
        self.maxScore = maxScore
        self.round = 0
        self.scoreLeft = 0
        self.scoreRight = 0
        self.ball = ball
        self.display = display
        self.rightScoreColor = rightScoreColor
        self.leftScoreColor = leftScoreColor
        self.win_width = win_width
        self.win_height = win_height
        self.margin = margin
        self.font = font
        self.largeFont = largeFont
        self.pygame = pygame
        self.background = background
        self.boundaryColor = boundaryColor
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.clock = clock
        self.rightPaddle = rightPaddle
        self.leftPaddle = leftPaddle

    def init(self):
        self.pygame.display.set_caption("Waiting from server ... ")
        self.boundary()

    def showScore(self):
        leftScoreText = self.font.render("Score : " + str(self.scoreLeft), True, self.leftScoreColor)
        rightScoreText = self.font.render("Score : " + str(self.scoreRight), True, self.rightScoreColor)

        self.display.blit(leftScoreText, (3*self.margin, 3*self.margin))
        self.display.blit(rightScoreText, (self.win_width/2 + 3*self.margin, 3*self.margin))


    def checkGameOver(self):
        if self.scoreLeft == self.maxScore or self.scoreRight == self.maxScore:
            while True:
                for event in self.pygame.event.get():
                    if event.type == self.pygame.QUIT:
                        self.close()
                    if event.type == self.pygame.KEYDOWN:
                        if event.key == self.pygame.K_q:
                            self.close()
                        if event.key == self.pygame.K_r:
                            self.reset()
                if self.scoreLeft == self.maxScore:
                    playerWins = self.largeFont.render("Left Player Wins!", True, self.leftScoreColor)
                elif self.scoreRight == self.maxScore:
                    playerWins = self.largeFont.render("Right Player Wins!", True, self.rightScoreColor)

                self.display.blit(playerWins, (self.win_width/2 - 100, self.win_height/2))
                self.pygame.display.update()


    def reset(self):
        self.scoreLeft = 0
        self.scoreRight = 0
        self.reset()


    def pause(self):
        pass


    def close(self):
        self.pygame.quit()
        sys.exit()


    def setPlayer(self, player: Player, send):
        self.player = player
        self.pygame.display.set_caption(f"Player {player.id} Ready !")
        self.send = send

    def onPlayerMove(self, change: int):
        self.send(json.dumps({self.player.id: {'change': change}}))


    def on_msg(self, data: str):
        msg = {}

        try:
            if '}{' in data:
                msg = json.loads('{' + data.split('}{')[-1])
            else:
                msg = json.loads(data)
            
            # print(msg)

        except:
            # pass
            print(f"Can't load: {data}")            


        if 'round' in msg:
            round = msg['round']

            print(round)

            if self.round <= round:
                self.round = round

                if "1" in msg:
                    x = msg["1"]['x']
                    y = msg["1"]['y']
                    self.leftPaddle.setPos(x, y)
                if "2" in msg:
                    x = msg["2"]['x']
                    y = msg["2"]['y']
                    self.rightPaddle.setPos(x, y)
                
                ballY = msg.get('ballY', None)
                ballX = msg.get('ballX', None)

                # print(ballX)
                # print(ballY)

                if ballX != None and ballY != None:
                    self.ball.setPos(ballX, ballY)
                    self.ball.checkForPaddle() 

                if "scoreLeft" in msg:
                    scoreLeft = msg["scoreLeft"]
                    self.scoreLeft = scoreLeft
                if "scoreRight" in msg:
                    scoreRight = msg["scoreRight"]
                    self.scoreRight = scoreRight
        
        self.display.fill(self.background)
        
        self.showScore()

        self.ball.show()
        self.leftPaddle.show()
        self.rightPaddle.show()

        self.boundary()

        self.checkGameOver()
        
        self.pygame.display.update()
        self.clock.tick(60)
        pass


    def start(self):
        while True:
            change = 0
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.close()
                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_q:
                        self.close()
                    if event.key == self.pygame.K_SPACE or event.key == self.pygame.K_p:
                        self.pause()
                    if event.key == self.pygame.K_r:
                        self.reset()
                    
                    if event.key == self.player.key_up:
                        change = -1
                    if event.key == self.player.key_down:
                        change = 1
                if change != 0:
                    self.onPlayerMove(change)

    def boundary(self):
        self.pygame.draw.rect(self.display, self.left, (0, 0, self.margin, self.win_height))
        self.pygame.draw.rect(self.display, self.top, (0, 0, self.win_width, self.margin))
        self.pygame.draw.rect(self.display, self.right, (self.win_width-self.margin, 0, self.margin, self.win_height))
        self.pygame.draw.rect(self.display, self.bottom, (0, self.win_height - self.margin, self.win_width, self.margin))

        l = 25
        
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 10, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 60, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 110, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 160, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 210, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 260, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 310, self.margin, l))
        self.pygame.draw.rect(self.display, self.boundaryColor, (self.win_width/2-self.margin/2, 360, self.margin, l))
