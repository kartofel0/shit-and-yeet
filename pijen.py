from player import Player

class Pijen(Player):
    def __init__(self, x, y, vel, shitNum):
        super().__init__(x, y, vel)
        self.shitNum = shitNum

    def getShitNum(self):
        return self.shitNum

    def shit(self):
        self.shitNum -= 1
        # drop shit