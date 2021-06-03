import socket
import time
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import time
import math
import random
import sympy

time.clock = time.process_time

HOST = '0.0.0.0'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('2'.encode())

print('Ballot Name: ', end='')
ballot = input()
f = open(ballot, 'r')
option = f.readline()[:-1]
pkc = f.readline()[:-1]
sig_ticket = f.readline()[:-1]
sig_pkc = f.readline()[:-1]
sig_hoption = f.readline()[:-1]

time.sleep(0.5)
s.send(option.encode())
time.sleep(0.5)
s.send(pkc.encode())
time.sleep(0.5)
s.send(sig_ticket.encode())
time.sleep(0.5)
s.send(sig_pkc.encode())
time.sleep(0.5)
s.send(sig_hoption.encode())
print(s.recv(1024).decode())
