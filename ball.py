from pong_constants import GameConstants
import random
import pyxel
from game_objects import PhysicalObject

class Ball (PhysicalObject):
    def __init__(self, x = GameConstants.WIDTH // 2, y = GameConstants.HEIGHT // 2): # default position in the middle of the screen
        Xvelocity, Yvelocity = self.getSpeed()
        super().__init__(
            name = "Ball"
            , x = x
            , y = y
            , width = GameConstants.BALL_SIZE
            , height = GameConstants.BALL_SIZE
            , Yvelocity = Yvelocity
            , Xvelocity = Xvelocity
        )
        self.is_running = False
        # self.player_who_scored = None

    def tick(self):
        if self.is_running:
            self.x += self.Xvelocity
            self.y += self.Yvelocity

    def reset(self):
        self.x = GameConstants.WIDTH // 2
        self.y = GameConstants.HEIGHT // 2
        self.Xvelocity, self.Yvelocity = self.getSpeed()
    
    def process(self):
        # Bounce off top and bottom walls
        if self.y <= 0 or self.y >= GameConstants.HEIGHT - self.width:
            self.Yvelocity = -self.Yvelocity

    def collision(self, object):
        # Bounce the ball
        if (self.x <= object.x + object.width 
            and self.x + self.width >= object.x
            and self.y + self.width >= object.y 
            and self.y <= object.y + object.height):
            self.Xvelocity = -self.Xvelocity  
    
    def render(self):
        pyxel.rect(self.x, self.y, self.width, self.width, GameConstants.AGENTS_COLOR)

    def getSpeed(self):
        return random.choice([GameConstants.BALL_SPEED, -GameConstants.BALL_SPEED]), random.choice([GameConstants.BALL_SPEED * .5, - (GameConstants.BALL_SPEED * .5)])