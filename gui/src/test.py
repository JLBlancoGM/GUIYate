"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""
from ServerManager import ServerManager
from UserManager import UserManager
from CallToServer import CallToServer
import time

def main():
    '''connect = UserManager('localhost', 'root', 'radio88', 'yate')
    connect.reset_table()
    print connect.list_users()'''
    server = ServerManager()
    call = CallToServer()
    server.run()
    time.sleep(1)
    call.stop_remote()

if __name__ == '__main__':
    main()