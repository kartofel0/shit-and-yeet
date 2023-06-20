import socket
import pygame
from _thread import *
import os
import sys
import time
from movingSprites import MovingSprites
from countdown import Countdown

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 5555
WHITE = (255,255,255)
GREY = (131,139,139)
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
my_socket.connect((IP_ADDR, PORT))

# get first data about self
data = my_socket.recv(1024).decode()
data = data.split(',')

player_type = data[0]
posX = float(data[1])
posY = float(data[2])
vel = float(data[3])
posXe = float(data[4])
posYe = float(data[5])
vele = float(data[6])

scale = 0.2

pjn_info = {'anim':True, 'w':7515, 'h':498, 'amount':15}
hmn_info = {'anim':False, 'w':8602, 'h':669, 'amount':23}
shitList = []    # [ [shit,rect,x,y], ... ]

if player_type == 'pjn':
    enemy_type = 'hmn'
    player_info = pjn_info
    enemy_info = hmn_info
    
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

def endGame(win, winner):
    print("got to end game")
    print("winner is", winner)
    text = font.render("END GAME", True, GREY)
    text_rect = text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    eg_win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
       win.blit(eg_win,(0,0))
       win.blit(text, text_rect)
       pygame.display.update()

    '''
    background_colour = (255,255,255)
    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tutorial 1')
    screen.fill(background_colour)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event. type == pygame.QUIT:
                running = False
    '''
    #windowSurface = pygame.display.set_mode((1000, 750), pygame.DOUBLEBUF)
    #s = pygame.Surface((1000,750))  # the size of your rect
    #s.set_alpha(128)                # alpha level
    #s.fill((255,255,255))           # this fills the entire surface
    #windowSurface.blit(s, (0,0))    # (0,0) are the top-left coordinates
    #Countdown(30)

# returns: anim, direction, posX
def Move(dir): #
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
    
    # type mov addX pWidth
    my_socket.send((player_type + ',mov,' + str(moveX) + ',' + str(player_info['w']/player_info['amount']*scale) + ',' + str(anim) + ',' + direction).encode()) # type mov movex pwidth anim direction

    # recieve updated pos
    updt = my_socket.recv(1024).decode()
    updt = updt.split(',')
    posX = updt[0]
    anime = updt[1]
    directione = updt[2]
    posXe = updt[3]

    return anim, direction, posX, anime, directione, posXe 

def DropShit(prev, shitList): #
    # if pressed shift send 'sht' etc

    sent = False
    t = time.time()
    #print('t - prev = ' + str(t-prev))
    if (t - prev > 1):
        can_shit = False
        data = []
        if player_type == 'pjn':

            keys = pygame.key.get_pressed()
            #if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            if keys[pygame.K_SPACE]:
                prev = t
                my_socket.send('pjn,sht'.encode())
                sent = True
                print('sent: ' + str(sent))
            
            if sent:
                # recieve position and draw shit
                data = my_socket.recv(1024).decode()
                print('drop shit recieved data: ' + data)
                #if data == 'no':
                #    pass
                #else:
                #    can_shit = True
                if data != 'no':
                    can_shit = True

        if can_shit:
            data = data.split(',')
            shit = MovingSprites('sht.png', 138, 522, 1)
            shitList.append([shit,shit.getRect(),str(float(data[0])+(pjn_info['w']/pjn_info['amount'])/2*scale),str(float(data[1])+pjn_info['h']/2*scale)])
            
    return sent, prev

def EliminateShit(shitList):
    sent = False
    winner = None
    #if player_type == 'pjn':
    if len(shitList) > 0:
        if shitList[0][0].getPosY() > WINDOW_HEIGHT - shitList[0][0].getHeight():
            shitList.pop(0)
            my_socket.send('pjn,rmv'.encode())
            sent = True
            if my_socket.recv(1024).decode() == 0:
                my_socket.send('end'.encode())    # run false
                winner = my_socket.recv(1024).decode()
            else:
                my_socket.send('ok'.encode())
    return sent, winner

def ShatOn(shitList):
    sent = False
    winner = None
    if player_type == ' hmn':
        rect = player.getRect()
        for shit in shitList:
            if rect.colliderect(shit[1]):
                my_socket.send('hmn,hit'.encode())    # run false
                winner = my_socket.recv(1024).decode()
                sent = True
                break
    return sent, winner

def redrawShit(): #[ [shit,rect,x,y], ... ]
    for shit in shitList:
        print('shit')
        shit[0].draw(win, float(shit[2]), float(shit[3])+5, False, 0.05)    # win x y false scale
        shit[1] = shit[0].getRect()
        shit[3] = shit[0].getPosY()
        #print(str(shit[0]))
        #shit[0].draw(win, 50, 200, False, 0.1)

def printText(content, clr, bgClr, anchor):
    text = font.render(content, True, clr, bgClr)
    textRect = text.get_rect()
    textRect.topleft = anchor
    return text, textRect

def redrawWindow(px, py, anim, scale, dir, ex, ey, anime, dire ,cntdwn):
    win.fill((255,255,255))

    now = cntdwn.getTime()
    if len(str(now)) == 1:
        now = '0' + str(now)
    text, textRect = printText('00:' + str(now), (0,0,0), None, (0,0))
    win.blit(text, textRect)

    player.draw(win, px, py, anim, scale, dir)
    enemy.draw(win, ex, ey, anime, scale, dire)
    #if player_type == 'pjn':
    redrawShit()

    pygame.display.update()

def main( ):
    run = True
    direction = 'l'
    clock = pygame.time.Clock()
    countdown_start = Countdown(3)
    countdown_game = Countdown(10)
    now = 0
    winner = None

    # start 3 sec timer
    # start thread 30 secs
    start_new_thread(countdown_game.startCountdown, ())

    while run and winner == None:
        clock.tick(60)

        # handle X button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                my_socket.close()

        if countdown_game.getTime() == 0:
            my_socket.send((player_type + ',end').encode())
            winner = my_socket.recv(1024).decode()
            print("winner is", winner)
            break
            #run = False
            #pygame.quit()

        # handle all functions
        ds, t = DropShit(now, shitList)
        now = t

        es, w1 = EliminateShit(shitList)
        so, w2 = ShatOn(shitList)

        if w1 != None:
            winner = w1
        if w2 != None:
            winner = w2

        if not (ds or es or so):
            anim, direction, posX, anime, directione, posXe = Move(direction)
        redrawWindow(posX, posY, anim, scale, direction, posXe, posYe, anime, directione,countdown_game)
        # anim, direction, posX = move()
        # redraw window     !!! draw(float(posX), float(posY), direction, anim, scale)
    endGame(win, winner)


        
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