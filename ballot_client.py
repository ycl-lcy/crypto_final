import socket
import time
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import time
import math
import random
import sympy
import hashlib

time.clock = time.process_time

HOST = '0.0.0.0'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('1'.encode())
print('username: ', end='')
username = input()
print('password: ', end='')
password = input()

ckey = RSA.generate(1024)

time.sleep(0.01)
s.send(username.encode())
time.sleep(0.01)
s.send(password.encode())
time.sleep(0.01)
s.send(str(ckey.e).encode())
time.sleep(0.01)
s.send(str(ckey.n).encode())
skey_e = int(s.recv(1024).decode())
skey_n = int(s.recv(1024).decode())

valid_projects = s.recv(1024).decode()
valid_projects = valid_projects.split('.')
valid_projects = [int(i) for i in valid_projects]
ss = 'Project List: '
for i in valid_projects:
    ss += str(i)+','
print(ss[:-1])
print('Choose Project: ', end='')
project_id = int(input())

ticket = str(project_id) + '00000' + str(pow(project_id, ckey.d, skey_e))
r = 94891562356475876273
pkc = int(str(ckey.n)+str(ckey.e))
pkc_b = (pkc*(r**skey_e)) % skey_n

time.sleep(0.01)
s.send(ticket.encode())
time.sleep(0.01)
s.send(str(pkc_b).encode())

sig_ticket = int(s.recv(1024).decode())
options = s.recv(1024).decode()
sig_pkc_b = int(s.recv(1024).decode())
r_1 = sympy.mod_inverse(r, skey_n)
sig_pkc = (sig_pkc_b * r_1) % skey_n

options = options.split('.')
options = [int(i) for i in options]
ss = 'Option List: '
for i in options:
    ss += str(i)+','
print(ss[:-1])
print('Choose Option: ', end='')
option = int(input())

sig_hoption = pow(int(hashlib.sha256(str(option).encode()).hexdigest(), 16), ckey.d, ckey.n)

print('Ballot Name: ', end='')
ballot = input()
f = open(ballot, 'w')
f.write(str(option)+'\n')
f.write(str(pkc)+'\n')
f.write(str(sig_ticket)+'\n')
f.write(str(sig_pkc)+'\n')
f.write(str(sig_hoption)+'\n')
