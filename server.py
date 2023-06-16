# client connected
# send window dimensions, who are you

import socket
from player import Player
from pijen import Pijen
from shit import Shit


IP_ADDR = '192.168.0.180'
PORT = 5555
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

playerNum = 0

pjn_vel = 3
hmn_vel = 3.3

pijen = Pijen(WINDOW_WIDTH/2, WINDOW_HEIGHT/5, pjn_vel, 5)
human = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT-100, hmn_vel)

shitList = []


#def endGame()








server_soc = socket.socket()
server_soc.bind((IP_ADDR, PORT))   #whoever tries to connect to that ip connects to that port
server_soc.listen(2)
print('Server started, waiting for connection')


while playerNum < 2:
    try:
        (client_soc, client_addr) = server_soc.accept() #returns tuple 1 - client's sockets object, 2 - tuple with client ip and port
        print('Client connected')
    except:
        print('couldn\'t connect client')


    # send window dimension, who are you
    if playerNum == 0:
        client_soc.send('pjn,{pjn_vel}'.encode())
        playerNum += 1
    elif playerNum == 1:
        client_soc.send('hmn,{hmn_vel}'.encode())
        playerNum += 1


# now begin game
client_soc.send('start'.encode())


# main game loop
winner = 'tie'    # when disconnected ig
run = True
while run:
    # data: ['???,mov,addX,pWidth']
    # data: ['pjn,sht']
    # data: ['hmn,hit']
    # data: ['???,end']
    data = client_soc.recv(1024).decode()
    data = data.split(',')
    #dataLen = len(data)
    type = data[0]
    action = data[1]
    try:
        addX = data[2]
        pWidth = data[3]
    except:
        pass
    


    match action:

        case 'mov':
            if type == 'pjn':
                pijen.updatePos(addX, 0, pWidth, WINDOW_WIDTH)
                reply = str(pijen.getPosX())
            elif type == 'hmn':
                human.updatePos(addX, 0, pWidth, WINDOW_WIDTH)
                reply = str(human.getPosX())
            # return updated pos
            client_soc.send(reply.encode())
        
        case 'sht':
            pass
            # create shit object, add to shitList as first
            # send to client position

        case 'rmv':    # shit reached floor, eliminate shit
            pass
            # remove first shit from list

        case 'hit':
            pass    # run false, winner = pjn wins

        case 'end':    # timer ended /  no more poops from pijen
            pass    # run false, winner = hmn wins

# endGame(winner)








#data = client_soc.recv(1024).decode()
#print("Client sent: " + data)

#reply = "Hello " + data
#client_soc.send(reply.encode())

client_soc.close() #closes connection with client
server_soc.close()
