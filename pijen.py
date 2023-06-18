from player import Player

class Pijen(Player):
    def __init__(self, x, y, vel, anim, direction, shitNum):
        super().__init__(x, y, vel, anim, direction)
        self.shitNum = shitNum

    def getShitNum(self):
        return self.shitNum

    def shit(self):
        self.shitNum -= 1
        # drop shit
