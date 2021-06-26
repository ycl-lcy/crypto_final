import socket
import time
import math
import random
import sympy
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

time.clock = time.process_time

f = open('accounts.txt', 'r')
a = f.read().split('\n')[3:]
f.close()

print('Choose Account: ', end='')
i = input()
username = a[int(i)][2:8]
pasword = a[int(i)][13:25]

ckey = RSA.generate(1024)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('0.0.0.0', 7777))

conn.send('1'.encode())

time.sleep(0.01)
conn.send(username.encode())
time.sleep(0.01)
conn.send(pasword.encode())
skey_e = int(conn.recv(1024).decode())
skey_n = int(conn.recv(1024).decode())

valid_projects = conn.recv(1024).decode()
valid_projects = valid_projects.split('.')
valid_projects = [int(i) for i in valid_projects]
s = 'Project List: '
for i in valid_projects:
    s += str(i)+','
print(s[:-1])
print('Choose Project: ', end='')
project_id = int(input())

ticket = str(project_id) + '00000' + str(pow(project_id, ckey.d, skey_e))
r = 94891562356475876273
pkc = int(str(ckey.n)+str(ckey.e))
pkc_b = (pkc*(r**skey_e)) % skey_n

time.sleep(0.01)
conn.send(ticket.encode())
time.sleep(0.01)
conn.send(str(pkc_b).encode())

sig_ticket = int(conn.recv(1024).decode())
options = conn.recv(1024).decode()
sig_pkc_b = int(conn.recv(1024).decode())
r_1 = sympy.mod_inverse(r, skey_n)
sig_pkc = (sig_pkc_b * r_1) % skey_n

options = options.split('.')
options = [int(i) for i in options]
s = 'Option List: '
for i in options:
    s += str(i)+','
print(s[:-1])
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
f.close()
