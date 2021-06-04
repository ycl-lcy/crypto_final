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

conn.send('3'.encode())
project_list = conn.recv(1024).decode()
project_list = project_list.split('.')
project_list = [int(i) for i in project_list]
s = 'Project List: '
for i in project_list:
    s += str(i)+','
print(s[:-1])

print("Choose Project: ", end='')
project_id = input()
time.sleep(0.01)
conn.send(str(project_id).encode())
result = conn.recv(1024*1000).decode()
print(result)
