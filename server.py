import pymysql.cursors
import random
import string
import sys
import socket
import time
import multiprocessing
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

time.clock = time.process_time

projects = [[]]*6
projects[1] = [1,2,3,4,5,6]
projects[3] = [1,2,5,6]
projects[4] = [1,2,4,5,6]
projects[5] = [1,2,3,5,6]

skey = RSA.generate(1024)

def server(conn):
    try:
        flag = conn.recv(1).decode() 
        connection = pymysql.connect(host='localhost',
                                         port=8888,
                                         user='root',
                                         password='supersecret',
                                         database='crypto_final',
                                         cursorclass=pymysql.cursors.DictCursor)

        if flag == '1':
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
     
            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT `password` FROM `users` WHERE `username`=%s"
                    cursor.execute(sql, (username,))
                    result = cursor.fetchone()
                    if result['password'] != hashlib.sha256(password.encode()).hexdigest():
                        exit()
               
                time.sleep(0.01)
                conn.send(str(skey.e).encode())
                time.sleep(0.01)
                conn.send(str(skey.n).encode())

                valid_projects = ''
                for i in range(len(projects)):
                    if len(projects[i]) != 0:
                        with connection.cursor() as cursor:
                            sql = "SELECT * FROM `signatures` WHERE `username`=%s and `projectID`=%s"
                            cursor.execute(sql, (username, i))
                            result = cursor.fetchone()
                            if not result:
                                valid_projects += '.'+str(i)

                valid_projects = valid_projects[1:]
                time.sleep(0.01)
                conn.send(valid_projects.encode())
                valid_projects = valid_projects.split('.')
                valid_projects = [int(i) for i in valid_projects]

                ticket = conn.recv(1024).decode()
                project_id = int(ticket[:ticket.find('00000')])
                ticket = int(ticket)
                if project_id not in valid_projects:
                    exit()

                sig_ticket = pow(ticket, skey.d, skey.n)
                time.sleep(0.01)
                conn.send(str(sig_ticket).encode())
                
                options = ""
                for i in projects[project_id]:
                    options += '.'+str(i)
                options = options[1:]
                time.sleep(0.01)
                conn.send(options.encode())
                
                pkc = int(conn.recv(1024).decode())
                sig_pkc = pow(pkc, skey.d, skey.n)
                time.sleep(0.01)
                conn.send(str(sig_pkc).encode())
                
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `signatures` (`username`, `projectID`, `sigPKC`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (username, project_id, str(sig_pkc)))
                connection.commit()

        elif flag == '2':
            option = int(conn.recv(1024).decode())
            pkc = int(conn.recv(1024).decode())
            sig_ticket = int(conn.recv(1024).decode())
            sig_pkc = int(conn.recv(1024).decode())
            sig_hoption = int(conn.recv(1024).decode())
            sig_pkc1 = pow(pkc, skey.d, skey.n)
            sig_pkc2 = sig_pkc

            ticket = str(pow(sig_ticket, skey.e, skey.n))
            project_id = int(ticket[:ticket.find('00000')])
            
            if option not in projects[project_id]:
                exit()

            if sig_pkc1 != sig_pkc2:
                exit()

            hoption1 = pow(sig_hoption, int(str(pkc)[-5:]), int(str(pkc)[:-5]))
            hoption2 = int(hashlib.sha256(str(option).encode()).hexdigest(), 16)
            if hoption1 != hoption2:
                exit()

            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `votes` WHERE `PKC`=%s"
                    cursor.execute(sql, (str(pkc)))
                    result = cursor.fetchone()
                    if result:
                        exit()

                with connection.cursor() as cursor:
                    sql = "INSERT INTO `votes` (`projectID`, `optionID`, `PKC`, `sigHoption`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (project_id, option, str(pkc), str(sig_hoption)))
                connection.commit()
                conn.send('Success'.encode())

        elif flag == '3':
            project_list = ''
            for i in range(len(projects)):
                if len(projects[i]) != 0:
                    project_list += '.'+str(i)
            project_list = project_list[1:]
            conn.send(project_list.encode())
            project_id = int(conn.recv(1024).decode())
            if not str(project_id) in project_list.split('.'):
                exit()

            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `votes` WHERE `projectID`=%s"
                    cursor.execute(sql, project_id)
                    result = cursor.fetchall()
                    conn.send(str(result).encode())
            
        else:
            print('bye')

    except ConnectionResetError:
        conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 7777))
s.listen(10)

while True:
    conn, addr = s.accept()
    m = multiprocessing.Process(target=server, args=(conn,))
    m.daemon = True
    m.start()

