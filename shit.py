from player import Player

class Shit(Player):
    def __init__(self, x, y, vel):
        super().__init__(x, y, vel)
        self.x = x
        self.y = y
        self.active = True

    # drop load from x y
    # fly down with certain velocity
    # when reaches ground deactivate

    def getActiveStatus(self):
        return self.active
    
    def deactivate(self):
        self.active = False

    def drop(self):
        pass

    def updatePos(self):
        pass
