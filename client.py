import socket
import pygame
from _thread import *
import os
import pickle
import time
from movingSprites import MovingSprites
from countdown import Countdown

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# draw window
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('shit n yeet')

font = pygame.font.Font('test_font.ttf', 20)

# draw floor
#floor_surface = pygame.Surface((WINDOW_WIDTH,50))
#floor_surface.set_alpha(128)
#floor_surface.fill((0,0,0))
#win.blit(floor_surface, (0,300))
#floor_rect = floor_surface.get_rect()
#print('floor surf: ' + str(floor_surface))
#print('floor rect: ' + str(floor_rect))


# connect to server
my_socket = socket.socket()
my_socket.connect(('192.168.0.180', 5555))

# get first data about self
data = my_socket.recv(1024).decode()
data = data.split(',')
#print(data[0] + ' - type, type: ' + str(type(data[0])))
#print(data[1] + ' - posX, type: ' + str(type(float(data[1]))))
#print(data[2] + ' - posY, type: ' + str(type(float(data[2]))))
#print(data[3] + ' - vel, type: ' + str(type(float(data[3]))))
#data[1] = float(data[1]) # posX
#data[2] = float(data[2]) # posY
#data[3] = float(data[3]) # vel
player_type = data[0]
posX = float(data[1])
posY = float(data[2])
vel = float(data[3])
posXe = float(data[4])
posYe = float(data[5])
vele = float(data[6])

scale = 0.2

#if player_type == 'pjn':
    #player_info = {'anim':True, 'w':7515, 'h':498, 'amount':15}
    #anim = True
    #w = 7515
    #h = 498
    #amount = 15
    #shitList = []    # [ [shit,rect,x,y], ... ]
#elif player_type == 'hmn':
    #player_info = {'anim':False, 'w':8602, 'h':669, 'amount':23}
    #anim = False
    #w = 8602
    #h = 669
    #amount = 23

pjn_info = {'anim':True, 'w':7515, 'h':498, 'amount':15}
hmn_info = {'anim':False, 'w':8602, 'h':669, 'amount':23}
shitImageList = []    # [ [shit,rect], ... ]
shitXY = []

if player_type == 'pjn':
    enemy_type = 'hmn'
    player_info = pjn_info
    enemy_info = hmn_info
#    player = MovingSprites('pjn.png', pjn_info['w'], pjn_info['h'], pjn_info['amount'])
#    enemy = MovingSprites('hmn.png', hmn_info['w'], hmn_info['h'], hmn_info['amount'])
elif player_type == 'hmn':
    enemy_type = 'pjn'
    player_info = hmn_info
    enemy_info = pjn_info
player = MovingSprites(player_type + '.png', player_info['w'], player_info['h'], player_info['amount'])
enemy = MovingSprites(enemy_type + '.png', enemy_info['w'], enemy_info['h'], enemy_info['amount'])



# wait for begin
wait = True
while wait:
    try:
        start = my_socket.recv(1024).decode()
        if start == 'start':
            print('recieved message to start')
            wait = False
    except:
        pass

# returns: anim, direction, posX
def Move(dir): #
    print('start move')
    moveX = 0
    direction = dir
    if player_type == 'hmn':
        anim = False
    else:
        anim = True

    yes = True
    while yes:
        keys = pygame.key.get_pressed()
        yes = False
    if keys[pygame.K_LEFT]:
        anim = True
        moveX -= vel 
        direction = 'l'
    if keys[pygame.K_RIGHT]:
        anim = True
        moveX += vel
        direction = 'r'
    #print('got key input')

    # type mov addX pWidth
    my_socket.send((player_type + ',mov,' + str(moveX) + ',' + str(player_info['w']/player_info['amount']*scale) + ',' + str(anim) + ',' + direction).encode()) # type mov movex pwidth anim direction
    print('sent data to server')

    # recieve updated pos
    updt = my_socket.recv(1024).decode()
    print('recieved data from server')
    if player_type == 'hmn':
        print(str(updt))
    updt = updt.split(',')
    posX = updt[0]
    anime = updt[1]
    directione = updt[2]
    posXe = updt[3]
    print('split data')

    print('end move')
    return anim, direction, posX, anime, directione, posXe
    
def rearrangeShitXY(shitXY):
    shitXY[0] = str(float(shitXY[0])+(pjn_info['w']/pjn_info['amount'])/2*scale)
    shitXY[1] = str(float(shitXY[1])+pjn_info['h']/2*scale)
    return shitXY

def DropShit(prev): #
    # if pressed shift send 'sht' etc

    sent = False
    t = time.time()
    #print('t - prev = ' + str(t-prev))
    if (t - prev > 1.15):
        #can_shit = False
        #data = []
        #if player_type == 'pjn':

        keys = pygame.key.get_pressed()
        #if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        if keys[pygame.K_SPACE]:
            if player_type == 'pjn':
                prev = t
            my_socket.send((player_type + ',sht').encode())
            sent = True
            #print('sent: ' + str(sent))
        
        if sent:
            # recieve position and draw shit
            #data = my_socket.recv(1024).decode()
            can = my_socket.recv(1024).decode()
            if can != 'no':
                shit = MovingSprites('sht.png', 138, 522, 1)
                shitImageList.append(shit)

            #try:
            #    s = s.decode()
            #except:
            #    shitXY = pickle.loads(s)
            #    shitXY = rearrangeShitXY(shitXY)
                #print('shitXY in dropshit: ' + str(shitXY))
            #print('drop shit recieved data: ' + data)
            #if data == 'no':
            #    pass
            #else:
            #    can_shit = True
            #if data != 'no':
            #    can_shit = True

        #if can_shit:
        #    data = data.split(',')
        #    shit = MovingSprites('sht.png', 138, 522, 1)
        #    shitImageList.append([shit,shit.getRect()])

            
    return sent, prev

def EliminateShit():
    sent = False
    winner = None
    #if player_type == 'pjn':
    if len(shitImageList) > 0:
        if shitImageList[0].getPosY() > WINDOW_HEIGHT - shitImageList[0].getHeight():
            shitImageList.pop()
            #shitXY = []
            print('shit eliminated')
            my_socket.send((player_type + ',rmv').encode())
            sent = True
            shtNum = my_socket.recv(1024).decode()
            if shtNum == 0:
                my_socket.send('end'.encode())    # run false
            else:
                my_socket.send('ok'.encode())
    return sent, winner

def ShatOn():
    sent = False
    winner = None
    if player_type == ' hmn':
        rect = player.getRect()
        #for shit in shitImageList:
        if rect.colliderect(shitImageList[0].getRect()):
            my_socket.send('hmn,hit'.encode())    # run false
            sent = True
            #break
    return sent, winner


def updateShit(shitImageList, shitXY):
    # if xy is full and images is not, add image
    # if xy is empty and image is not, remove image
    xy = len(shitXY)
    img = len(shitImageList)
    if xy == 0 and img != 0:
        shitImageList.clear()
        # remove
    elif xy != 0 and img == 0:
        shitImageList.append(MovingSprites('sht.png', 138, 522, 1))
        # add
    return shitImageList

def redrawShit(x, y): #[ [shit,rect,x,y], ... ]
    #for i in range(len(shitImageList)):
    #for shit in shitImageList:
    #if len(shitImageList) != 0:
    #print(str(shitXY))
    print('redraw shit')
    
    #shit = shitImageList[0]
        #print('shitXY in redraw shit' + str(shitXY))
        #print(str(type(shitXY[0])) + ', ' + str(type(shitXY[1])))
    shitImageList[0].draw(win, float(x), float(y)+5, False, 0.05)
        #shit[1] = shit[0].getRect()
    #my_socket.send(str(shitImageList[0].getPosY()).encode())
    #shitXY[1] = shitImageList[0].getPosY()
        #return shitXY
    #else:
    #    print('no shit')
        #return []
    #return shitXY
    #for shit in shitList:
    #    print('shit')
    #    shit[0].draw(win, float(shit[2]), float(shit[3])+5, False, 0.05)    # win x y false scale
    #    shit[1] = shit[0].getRect()
    #    shit[3] = shit[0].getPosY()
        #print(str(shit[0]))
        #shit[0].draw(win, 50, 200, False, 0.1)

def printText(content, clr, bgClr, anchor):
    text = font.render(content, True, clr, bgClr)
    textRect = text.get_rect()
    textRect.topleft = anchor
    return text, textRect

def redrawWindow(px, py, anim, scale, dir, ex, ey, anime, dire, cntdwn):
    if len(shitImageList) != 0:
        xy = my_socket.recv(1024).decode()
        xy = xy.split(',')

    win.fill((255,255,255))

    now = cntdwn.getTime()
    if len(str(now)) == 1:
        now = '0'+str(now)
    text, textRect = printText('00:'+str(now), (0,0,0), None, (0,0))
    win.blit(text, textRect)

    player.draw(win, px, py, anim, scale, dir)
    enemy.draw(win, ex, ey, anime, scale, dire)
    #if player_type == 'pjn':
    if len(shitImageList) != 0:
        redrawShit(xy[0], xy[1])

    pygame.display.update()


def main():
    run = True
    direction = 'l'
    clock = pygame.time.Clock()
    countdown_start = Countdown(3)
    countdown_game = Countdown(30)
    now = 0
    shit_count = 0
    winner = None

    # start 3 sec timer
    # start thread 30 secs
    start_new_thread(countdown_game.startCountdown, ())

    while run and winner == None:
        #print('start frame')
        clock.tick(60)

        # handle X button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                my_socket.close()

        if countdown_game.getTime() == 0:
            my_socket.send('end'.encode())
            winner = 'hmn'
            #pygame.quit()

        # handle all functions
        #print('before eliminate shit')
        es, w1 = EliminateShit()
        #print('after eliminate shit')
        #shitImageList = updateShits(shitImageList, shitInfoList)
        so, w2 = ShatOn()

        if not (es or so):
            ds, t = DropShit(now)
            #shitImageList = updateShits(shitImageList, shitInfoList)
            now = t

        #print('before update shit')
        #updateShit(shitImageList, shitXY)
        #print('after update shit')
        

        if w1 != None:
            winner = w1
        if w2 != None:
            winner = w2

        print('before move')
        if not (ds or es or so):
            print('inside if')
            anim, direction, posX, anime, directione, posXe = Move(direction)
        print('after move')
        #print('before redraw window')
        redrawWindow(posX, posY, anim, scale, direction, posXe, posYe, anime, directione, countdown_game)
        #print('after redraw window')
        # anim, direction, posX = move()
        # redraw window     !!! draw(float(posX), float(posY), direction, anim, scale)
        es = False
        so = False
        ds = False
        #print('end frame')

    #endGame(winner)
    pygame.quit()


#        newX = my_socket.recv(1024).decode()
#    if player == 'hmn':
#        my_socket.send('hit'.encode())
#    if player == 'pjn':
#        my_socket.send('sht'.encode())
#        shtLoc = my_socket.recv(1024).decode()

#my_socket.send('end'.encode())
#my_socket.close()
main()