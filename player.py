class Player():
    def __init__(self, x, y, vel=0):
        self.x = x
        self.y = y
        self.vel = vel

    def getPosX(self):
        return self.x
    
    def getPosY(self):
        return self.y
    
    def updatePos(self, addX, addY, pWidth=0, winWidth=0):
        self.x += float(addX)
        self.y += float(addY)
        if self.x <= 0:
            self.x = 0
        elif self.x > winWidth - pWidth:
            self.x = winWidth - pWidth
