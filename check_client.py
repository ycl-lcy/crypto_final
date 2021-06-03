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

s.send('3'.encode())
project_list = s.recv(1024).decode()
project_list = project_list.split('.')
project_list = [int(i) for i in project_list]
ss = 'Project List: '
for i in project_list:
    ss += str(i)+','
print(ss[:-1])
print("Choose Project: ", end='')
project_id = input()
time.sleep(0.01)
s.send(str(project_id).encode())
result = s.recv(1024*1000).decode()
print(result)
