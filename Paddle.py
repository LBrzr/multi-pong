class Paddle:
    def __init__(self, position, win_width, win_height, margin, pygame, color, display):
        self.w = 10
        self.h = self.w*8
        self.paddleSpeed = 12

        self.pygame = pygame

        self.display = display

        self.color = color
        
        self.position = position

        if position == -1:
            self.x = 1.5*margin
        else:
            self.x = win_width - 1.5*margin - self.w
            
        self.y = win_height/2 - self.h/2

        self.win_height = win_height

    
    def show(self):
        self.pygame.draw.rect(self.display, self.color, (self.x, self.y, self.w, self.h))

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def move(self, ydir):
        self.y += self.paddleSpeed*ydir
        if self.y < 0:
            self.y -= self.paddleSpeed*ydir
        elif self.y + self.h> self.win_height:
            self.y -= self.paddleSpeed*ydir