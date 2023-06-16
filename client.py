import socket
import pygame

my_socket = socket.socket()
my_socket.connect(('192.168.0.181', 5555))  #connects to a socket in that location

#my_socket.send('Omer'.encode())
data = my_socket.recv(1024).decode()
player, vel = data.split(',')
#print('The server sent: ' + data)

def Move():
    moveX = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        moveX -= vel 
    if keys[pygame.K_RIGHT]:
        moveX += vel
    
    my_socket.send('{player},{moveX}'.encode())
    # recieve updated pos, draw

def Drop():    # if pijen
    # if pressed shift send 'sht' etc
    pass

def EliminateShit():
    # if floor collides with st \/ send 'rmv'
    pass

def ShatOn():    # if human
    # if collided with st (/more than on object (floor + shit)) send 'hit' etc
    pass


# if sendning 'hit' or 'end'

def main( ):
    run = True
    while run:
        pass


#        newX = my_socket.recv(1024).decode()
#    if player == 'hmn':
#        my_socket.send('hit'.encode())
#    if player == 'pjn':
#        my_socket.send('sht'.encode())
#        shtLoc = my_socket.recv(1024).decode()

#my_socket.send('end'.encode())
#my_socket.close()
