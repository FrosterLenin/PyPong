import pyxel
from pong_constants import GameConstants  
from game_objects import PhysicalObject

class Player(PhysicalObject):
    def __init__(self, x, controls, name):
        super().__init__(
            name = name
            , x = x
            , y = GameConstants.HEIGHT // 2 - GameConstants.PADDLE_HEIGHT // 2
            , width = GameConstants.PADDLE_WIDTH
            , height = GameConstants.PADDLE_HEIGHT
            , Yvelocity = GameConstants.MOVEMENT_SPEED
            , Xvelocity = GameConstants.MOVEMENT_SPEED
        )
        self.controls = controls # commmands of each player
        self.points = 0

    def tick(self):
        if pyxel.btn(self.controls["up"]) and self.y > 0:
            self.y -= self.Yvelocity
        if pyxel.btn(self.controls["down"]) and self.y < GameConstants.HEIGHT - self.height:
            self.y += self.Yvelocity

    def process(self):
        if self.y < 0:
            self.y = 0
        if self.y > GameConstants.HEIGHT - self.height:
            self.y = GameConstants.HEIGHT - self.height


class FirstPlayer(Player):
    def __init__(self):
        super().__init__(10, {"up": pyxel.KEY_W, "down": pyxel.KEY_S}, "Player 1")
    def render(self):
        pyxel.rect(self.x, self.y, self.width, self.height, GameConstants.AGENTS_COLOR) 
        pyxel.text(self.x, self.x, f"{self.name}: {self.points}", GameConstants.AGENTS_COLOR)

class SecondPlayer(Player):
    def __init__(self):
         super().__init__(GameConstants.WIDTH - GameConstants.PADDLE_WIDTH - 10, {"up": pyxel.KEY_UP, "down": pyxel.KEY_DOWN}, "Player 2")
    def render(self):
        pyxel.rect(self.x, self.y, self.width, self.height, GameConstants.AGENTS_COLOR) 
        pyxel.text(GameConstants.WIDTH - (len(self.name)+50), 10, f"{self.name}: {self.points}", GameConstants.AGENTS_COLOR)

