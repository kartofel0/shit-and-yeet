import pygame

class Button():
    def __init__ (self, x, y, width, height, color, backColor, content, fontSize):
        self.font = pygame.font.Font('VoodooVampire.ttf', fontSize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.backColor = backColor

        #self.image = pygame.display.set_mode((self.width, self.height))
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.backColor)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.color)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def isPrassed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    def transparentBackGround(self):
        self.backColor = pygame.Surface((self.width, self.height), pygame.SRCALPHA)