import pygame

class MovingSprites():
    def __init__(self, spritesheet_name, width, height, amount):
        #self.spritesheet = pygame.image.load(spritesheet_name).convert()
        self.spritesheet = pygame.image.load(spritesheet_name).convert_alpha()
        self.spritesheet.set_colorkey((0,0,0))
        self.ssw = width
        self.ssh = height
        self.amount = amount
        '''
        self.images = []
        for i in range(0, self.amount):
            img = self.getImage(i*(self.ssw/self.amount), 0, self.ssw/self.amount, self.ssh)
            self.images.append(img)
        print('list len of sprites: ' + str(len(self.images)))
        '''
        self.images = self.divideSpritesheet(0, 0, self.ssw/amount, self.ssh, amount)
        #print(len(self.images))
        self.cur_sprite = 0
        self.image = self.images[self.cur_sprite]
        self.rect = self.image.get_rect()


    def divideSpritesheet(self, sprite_start_x,sprite_start_y,sprite_size_x,sprite_size_y,sheet_frames):
    #def slice_sheet(self,sprite_sheet,sprite_start_x,sprite_start_y,sprite_size_x,sprite_size_y,sheet_frames):
        frames = []
        sheet_start = 1 
        #frame_pos = 0
        sprite_start_x_base = sprite_size_x
        while sheet_start <= sheet_frames:
            sheet = self.spritesheet
            sheet.set_clip(pygame.Rect(sprite_start_x,sprite_start_y,sprite_size_x,sprite_size_y))
            sprite_clip = sheet.subsurface(sheet.get_clip())
            frames.append(sprite_clip)
            sprite_start_x += sprite_start_x_base
            sheet_start += 1
        return frames

    def getRect(self):
        return self.rect
    
    def getPosY(self):
        return self.y


    def getImage(self, posX, posY, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (posX, posY, width, height))
        image.set_colorkey((0,0,0))
        return image
    

    def update(self, anim, scale, dir):
        if anim:
            self.cur_sprite += 0.05
            if int(self.cur_sprite) == self.amount-1:
                self.cur_sprite = 0
        else:
            self.cur_sprite = self.amount-1

        #print('current sprite num: ' + str(int(self.cur_sprite+1)) + ' out of ' + str(len(self.images)))

        self.image = self.images[int(self.cur_sprite)]
        self.image = pygame.transform.scale_by(self.image, scale)
        if dir == 'r':
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()


    def draw(self, win, x, y, anim, scale, dir=None):
        #self.x = float(x)
        self.y = float(y)
        x = float(x)
        y = float(y)
        self.update(anim, scale, dir)
        win.blit(self.image, (x,y))
