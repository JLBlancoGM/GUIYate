"""
Created on 20/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""
import telnetlib
import logging
import os


class CallToServer():
    def __init__(self, host='0', port='5038'):
        self.host = host
        self.port = port

    def stop_remote(self):
        if os.path.isfile('pid'):
            try:
                tln = telnetlib.Telnet(self.host, self.port)
                print tln.read_until('\n')
            except Exception as err:
                logging.error(err)
                return 'Error in server conection', 1
            logging.info('Try send call to server')
            tln.write('stop')
        else:
            logging.info('The server is not running')
            return 'Error, the server is not running', 1

