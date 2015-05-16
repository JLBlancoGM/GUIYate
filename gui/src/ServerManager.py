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

from logConfig import *

init_logger(const.LOG_FILE)


class ServerManager(object):
    def __init__(self):
        self.is_start = False
        self.pid = None
        self.start_time = 0
        self.yate = os.path.isfile(const.YATE+'/run')
        self.get_pid()

    def get_pid(self):
        if not self.yate:
            logging.error('The yate sip server is not installed')
            return 'Error, yate sip server is not installed', 1
        try:
            self.pid = sub.check_output(['pidof', 'yate'])
        except sub.CalledProcessError, err:
            self.pid = None
            self.is_start = False
            logging.info(err)
            return 'Error to get pid', 0
        if self.pid:
            self.is_start = True
            return 'Ok, yate pit = ' + self.pid, 0
        else:
            self.is_start = False
            return 'Ok, yate pit = None ', 0

    def run(self, timeout=0.1):
        if not self.yate:
            logging.error('The yate sip server is not installed')
            return 'Error, yate sip server is not installed', 1
        self.get_pid()
        if not self.is_start:
            try:
                sub_popen = sub.Popen(['./run', '-d'], cwd=const.YATE)
                sub_popen.wait()
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
            with open(const.PID_SIP_FILE, 'w') as f:
                f.write(self.pid)
            return 'Server running', 0
        else:
            logging.info('The server already is running')
            return 'Server running', 0

    def stop(self):
        if not self.yate:
            logging.error('The yate sip server is not installed')
            return 'Error, yate sip server is not installed', 1
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
                os.remove(const.PID_SIP_FILE)
            except OSError, err:
                logging.error(err)
            return 'Ok, server stoped', 0
        else:
            logging.info('The server is not running')
            return 'Ok', 0

    def get_status(self):
        if not self.yate:
            logging.error('The yate sip server is not installed')
            return 'Error, yate sip server is not installed', 1
        now = time.time()
        if self.is_start:
            time_use = now - self.start_time
        else:
            time_use = 0
        return self.is_start, time_use

    def restart(self):
        if not self.yate:
            logging.error('The yate sip server is not installed')
            return 'Error, yate sip server is not installed', 1
        ret_stop = self.stop()
        ret_start = self.run()
        return ret_stop, ret_start


