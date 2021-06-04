import socket
import time
import math
import random
import sympy
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

time.clock = time.process_time

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('0.0.0.0', 7777))

conn.send('2'.encode())

print('Ballot Name: ', end='')
ballot = input()
f = open(ballot, 'r')
option = f.readline()[:-1]
pkc = f.readline()[:-1]
sig_ticket = f.readline()[:-1]
sig_pkc = f.readline()[:-1]
sig_hoption = f.readline()[:-1]
f.close()

time.sleep(0.5)
conn.send(option.encode())
time.sleep(0.5)
conn.send(pkc.encode())
time.sleep(0.5)
conn.send(sig_ticket.encode())
time.sleep(0.5)
conn.send(sig_pkc.encode())
time.sleep(0.5)
conn.send(sig_hoption.encode())
print(conn.recv(1024).decode())
