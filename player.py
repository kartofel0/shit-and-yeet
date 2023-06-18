class Player():
    def __init__(self, x, y, vel, anim, direction):
        self.x = x
        self.y = y
        self.vel = vel
        self.anim = anim
        self.direction = direction

    def getPosX(self):
        return self.x
    
    def getPosY(self):
        return self.y
    
    def getAnim(self):
        return self.anim
    
    def getDir(self):
        return self.direction
    
    def setAnim(self, a):
        self.anim = a
    
    def setDir(self, d):
        self.direction = d
    
    def updatePos(self, addX, addY, pWidth=0, winWidth=0):
        self.x += float(addX)
        self.y += float(addY)
        if self.x <= 0:
            self.x = 0
        elif self.x > winWidth - pWidth:
            self.x = winWidth - pWidth
