class Player():
    def __init__(self, x, y, vel=0):
        self.x = x
        self.y = y
        self.vel = vel

    def getPos(self):
        return self.x, self.y
    
    def updatePos(self, addX, addY, winWidth=0, pWidth=0):
        self.x += addX
        self.y += addY
        if self.x < pWidth/2:
            self.x = pWidth/2
        elif self.x > winWidth - pWidth/2:
            self.x = winWidth - pWidth/2