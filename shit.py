from player import Player

class Shit(Player):
    def __init__(self, x, y, floorY):
        self.x = x
        self.y = y
        #self.vel = 3
        self.floorY = floorY
        self.active = True

    # drop load from x y
    # fly down with certain velocity
    # when reaches ground deactivate

    def getActiveStatus(self):
        return self.active

    def drop(self):
        pass