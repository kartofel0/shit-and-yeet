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

pijen = Pijen(WINDOW_WIDTH/2, WINDOW_HEIGHT/5, 3, 5)
person = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT-100, 3.3)

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
        client_soc.send('{WINDOW_WIDTH},{WINDOW_HEIGHT},pjn'.encode())
        playerNum += 1
    elif playerNum == 1:
        client_soc.send('{WINDOW_WIDTH},{WINDOW_HEIGHT},hmn'.encode())
        playerNum += 1


# sign to begin game
client_soc.send('ok'.encode())









#data = client_soc.recv(1024).decode()
#print("Client sent: " + data)

#reply = "Hello " + data
#client_soc.send(reply.encode())

client_soc.close() #closes connection with client
server_soc.close()