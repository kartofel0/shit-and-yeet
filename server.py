import socket
from _thread import *
import threading
from player import Player
from pijen import Pijen
from shit import Shit


IP_ADDR = '192.168.0.180'
PORT = 5555
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

playerNum = 0

posX = WINDOW_WIDTH/2
#
pjnY = WINDOW_HEIGHT/5
pjn_vel = 3
pjn_anim = True
#
hmnY = WINDOW_HEIGHT-100
hmn_vel = 3.3
hmn_anim = False

pijen = Pijen(posX, pjnY, pjn_vel, pjn_anim, 'l', 5)
human = Player(posX, hmnY, hmn_vel, hmn_anim, 'l')

client_socs = []



def threaded_client(client_soc, num):
    # now begin game
    print('sending start to client ' + str(num))
    client_soc.send('start'.encode())

    # main game loop
    winner = 'tie'    # when disconnected ig
    run = True
    while run:
        # data: ['???,mov,addX,pWidth']
        # data: ['pjn,sht']
        # data: ['pjn,rmv']
        # data: ['hmn,hit']
        # data: ['???,end']
        data = client_soc.recv(1024).decode()
        if data != None and data != '':
            print('message from client: ' + data)
            data = data.split(',')
            type = data[0]
            action = data[1]
            try:
                addX = float(data[2])
                pWidth = float(data[3])
                anim = bool(data[4])
                direction = data[5]
                if type == 'pjn':
                    pijen.setAnim(anim)
                    pijen.setDir(direction)
                elif type == 'hmn':
                    human.setAnim(anim)
                    human.setDir(direction)
            except:
                pass
                #print(type + ' sent a message: ' + action + ', no add ons')
        


        match action:

            case 'mov':
                if type == 'pjn':
                    pijen.updatePos(addX, 0, pWidth, WINDOW_WIDTH)
                    reply = str(pijen.getPosX()) + ',' + str(human.getAnim()) + ',' + human.getDir() + ',' + str(human.getPosX()) # anim direction posx
                elif type == 'hmn':
                    human.updatePos(addX, 0, pWidth, WINDOW_WIDTH)
                    reply = str(human.getPosX()) + ',' + str(pijen.getAnim()) + ',' + pijen.getDir() + ',' + str(pijen.getPosX())
                # return updated pos
                client_soc.send(reply.encode())
            
            case 'sht':
                x = pijen.getPosX()
                y = pijen.getPosY()
                #shitList.insert(0, Shit(x, y, 4))
                if pijen.getShitNum() == 0:
                    print('no more pijen shits left sorry hehe')
                    reply = 'no'
                else:
                    pijen.shit()
                    reply = str(x) + ',' + str(y)
                client_soc.send(reply.encode())

            case 'rmv':    # shit reached floor, eliminate shit
                reply = pijen.getShitNum()
                client_soc.send(str(reply).encode())
                if client_soc.recv(1024).decode() == 'end':
                    print('no more shits, human wins') # run false, winner = hmn wins
                    run = False

            case 'hit':
                print('human shat on, pijen wins')    # run false, winner = pjn wins
                run = False

            case 'end':    # timer ended
                print('time ended, human wins')    # run false, winner = hmn wins
                run = False

        action = ''
    # endGame(winner)








    #data = client_soc.recv(1024).decode()
    #print("Client sent: " + data)

    #reply = "Hello " + data
    #client_soc.send(reply.encode())

    client_soc.close() #closes connection with client
    server_soc.close()

#def endGame() !!!!!!!!!!!!!!!!!!!!!!!!!!!!







server_soc = socket.socket()
server_soc.bind((IP_ADDR, PORT))
server_soc.listen(2)
print('Server started, waiting for connection')


# connect to 2 players
while playerNum < 2:
    try:
        client_soc, client_addr = server_soc.accept()    # start new thread
        print('Client ' + str(playerNum) + ' connected')
        client_socs.append(client_soc)

        if playerNum == 0:
            #client_soc.send(('pjn,' + str(posX) + ',' + str(pjnY) + ',' + str(pjn_vel)).encode())
            reply = ('pjn,' + str(posX) + ',' + str(pjnY) + ',' + str(pjn_vel) + ',' + str(posX) + ',' + str(hmnY) + ',' + str(hmn_vel))
            #playerNum += 1
        elif playerNum == 1:
            #client_soc.send(('hmn,' + ',' + str(posX) + ',' + str(hmnY) + ',' + str(hmn_vel)).encode())
            reply = ('hmn,' + str(posX) + ',' + str(hmnY) + ',' + str(hmn_vel) + ',' + str(posX) + ',' + str(pjnY) + ',' + str(pjn_vel))
            #playerNum += 1
        print( 'sending reply info to client ' + str(playerNum))
        client_soc.send(reply.encode())
        playerNum += 1
    except:
        print('couldn\'t connect client' + str(playerNum))


    # accept window dimensions
    #win_dimensions = client_soc.recv(1024).decode().split(',')
    #WINDOW_WIDTH = float(win_dimensions[0])
    #WINDOW_HEIGHT = float(win_dimensions[1])
    
    # send who are you, xpos, ypos, velocity
    #if playerNum == 0:
    #    #client_soc.send(('pjn,' + str(posX) + ',' + str(pjnY) + ',' + str(pjn_vel)).encode())
    #    reply = ('pjn,' + str(posX) + ',' + str(pjnY) + ',' + str(pjn_vel))
    #    #playerNum += 1
    #elif playerNum == 1:
    #   #client_soc.send(('hmn,' + ',' + str(posX) + ',' + str(hmnY) + ',' + str(hmn_vel)).encode())
    #    reply = ('hmn,' + str(posX) + ',' + str(hmnY) + ',' + str(hmn_vel))
    #    #playerNum += 1
    #print( 'sending reply info to client ' + str(playerNum))
    #client_soc.send(reply.encode())
    #playerNum += 1

def peepeepoopoo(info):
    print(info)


print('starting threads')
#t1 = threading.Thread(target = peepeepoopoo, args = ('itsa me',))
#t2 = threading.Thread(target = peepeepoopoo, args = ('mario',))
t1 = threading.Thread(target = threaded_client, args = (client_socs[0], 1))
t2 = threading.Thread(target = threaded_client, args = (client_socs[1], 2))
thrd = True
run_threads = True
while run_threads:
    if thrd:
        t1.start()
        t2.start()
        #start_new_thread(threaded_client, (client_socs[0], 1))
        #start_new_thread(threaded_client, (client_socs[1], 2))
        thrd = False
    if threading.active_count() < 2:
        print('less than 2 threads, stopped threading')
        run_threads = False
