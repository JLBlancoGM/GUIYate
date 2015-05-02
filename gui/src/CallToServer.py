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
import socket


class CallToServer():
    def __init__(self, host='0', port='5038'):
        self.host = host
        self.port = port
        connect_ok = 'ready on ' + socket.gethostname() + '.'
        connect_fail = 'Connection refused\n'
        self.connect_msg = [connect_ok, connect_fail]

    def try_connect(self):
        try:
            tln = telnetlib.Telnet(self.host, self.port)
        except Exception as err:
            logging.error(err)
            return 'Error in server conection', 1, None
        server_return = tln.expect(self.connect_msg, 2)
        if server_return[0] == 0:
            return 'Ok, connected to server', 0, tln
        else:
            return 'Error, connection refused', 1, None

    def stop_remote(self):
        conn = self.try_connect()
        if conn[1] == 0:
            logging.info('Try send call to server')
            conn[2].write('stop\r\n')
            ret = conn[2].expect(['Engine shutting down - bye!', ], 2)
            if ret[0] == 0:
                logging.info('Server shutdown')
                return 'Ok, server shutdown', 0
        else:
            return 'Error, shutting fail', 1

    def generic_comnand(self, call, expect_list):
        conn = self.try_connect()
        if conn[1] == 0:
            logging.info('Try send call to server')
            conn[2].write(call+'\r\n')
            exp = conn[2].expect(expect_list, 3)
            print exp
