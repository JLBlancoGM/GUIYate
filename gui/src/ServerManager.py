"""
Created on 17/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 01
SUMARY:  
"""
import logging
import const
import time
import os
import subprocess as sub


class ServerManager(object):
    def __init__(self):
        self.is_start = False
        self.pid = None
        self.start_time = 0
        self.get_pid()

    def get_pid(self):
        try:
            self.pid = sub.check_output(['pidof', 'yate'])
        except sub.CalledProcessError, err:
            self.pid = None
            self.is_start = False
            logging.info(err)
            return 'Error to get pid', 1
        if self.pid:
            self.is_start = True
            return 0
        else:
            self.is_start = False
            return 0

    def run(self, timeout=0.1):
        self.get_pid()
        if not self.is_start:
            try:
                sub.Popen(['./run', '-d'], cwd=const.YATE)
            except OSError, err:
                logging.error('Error, ' + str(err))
                return 'Error', 1
            self.start_time = time.time()
            while not self.is_start:
                self.get_pid()
                now_time = time.time()
                if now_time - self.start_time > timeout:
                    logging.error('Error to start server (timeout)')
                    return 'Error timeout', 1
            logging.info('Ok, the server is now running')
            with open('pid', 'w') as f:
                f.write(self.pid)
            return 'Server running', 0
        else:
            logging.info('The server already is running')
            return 'Server running', 0

    def stop(self):
        self.get_pid()
        if self.is_start:
            try:
                os.kill(int(self.pid), sub.signal.SIGKILL)
            except IOError:
                logging.error('Error to stop server')
                return 'Error to stop server', 1
            self.pid = None
            self.is_start = False
            logging.info('Ok, server stoped')
            try:
                os.remove('pid')
            except OSError, err:
                logging.error(err)
            return 'Ok, server stoped', 0
        else:
            logging.info('The server is not running')
            return 'Ok', 0

    def get_status(self):
        now = time.time()
        if self.is_start:
            time_use = now - self.start_time
        else:
            time_use = 0
        return self.is_start, time_use

    def restart(self):
        ret_stop = self.stop()
        ret_start = self.run()
        return ret_stop, ret_start


