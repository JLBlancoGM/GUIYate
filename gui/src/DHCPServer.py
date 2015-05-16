"""
Created on 27/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""
import const
import logging
import os
import subprocess as sub
import time


class DHCPServer(object):
    def __init__(self):
        self.is_start = False
        self.pid = None
        self.start_time = 0
        self.dhcp = os.path.isfile(const.DHCP+'/sbin/dhcpd')
        self.get_pid()
        self.root = self.is_root()

    def is_root(self):
        id = os.getuid()
        if id == 0:
            return True
        else:
            return False

    def get_pid(self):
        if not self.dhcp:
            logging.error('The dhcp server is not installed')
            return 'Error, dhcp server is not installed', 1
        try:
            self.pid = sub.check_output(['pidof', 'dhcpd'])
        except sub.CalledProcessError, err:
            self.pid = None
            self.is_start = False
            logging.info(err)
            return 'Error to get pid', 0
        if self.pid:
            self.is_start = True
            return 'Ok, dhcp pit = ' + self.pid, 0
        else:
            self.is_start = False
            return 'Ok, dhcp pit = Null' + self.pid, 0

    def run(self, timeout=0.1):
        if not self.root:
            logging.error('User without permissions')
            return 'Error, only root has permission to start the server', 1
        if not self.dhcp:
            logging.error('The dhcp server is not installed')
            return 'Error, dhcp server is not installed', 1
        self.get_pid()
        if not self.is_start:
            try:
                dhcpd = [const.DHCP+'/sbin/dhcpd', '-cf', '../etc/dhcpd.conf',
                         '-lf', '../db/dhcpd.leases', '-d']
                subPopen = sub.Popen(dhcpd, cwd=const.DHCP+'/sbin/')
                subPopen.wait()
            except OSError, err:
                logging.error('Error '+str(err))
                return 'Error', 1
            self.start_time = time.time()
            while not self.is_start:
                self.get_pid()
                now_time = time.time()
                if now_time - self.start_time > timeout:
                    logging.error('Error to start dhcp server (timeout)')
                    return 'Error timeout', 1
            logging.info('Ok, the dhcp server is now running')
            with open(const.PID_DHCP_FILE, 'w') as f:
                f.write(self.pid)
            return 'Server running', 0
        else:
            logging.info('The server already is running')
            return 'Server running', 0

    def stop(self):
        if not self.dhcp:
            logging.error('The dhcp server is not installed')
            return 'Error, sip server is not installed', 1
        self.get_pid()
        if self.is_start:
            try:
                os.kill(int(self.pid), sub.signal.SIGKILL)
            except IOError:
                logging.error('Error to stop dhcp server')
                return 'Error to stop server', 1
            self.pid = None
            self.is_start = False
            logging.info('Ok, dhcp server stoped')
            try:
                os.remove(const.PID_DHCP_FILE)
            except OSError, err:
                logging.error(err)
            return 'Ok, dhcp server stoped', 0
        else:
            logging.info('The dhcp server is not running')
            return 'Ok', 0

    def get_status(self):
        if not self.dhcp:
            logging.error('The dhcp server is not installed')
            return 'Error, dhcp server is not installed', 1
        now = time.time()
        if self.is_start:
            time_use = now - self.start_time
        else:
            time_use = 0
        return self.is_start, time_use

    def restart(self):
        if not self.dhcp:
            logging.error('The dhcp server is not installed')
            return 'Error, dhcp server is not installed', 1
        ret_stop = self.stop()
        ret_start = self.run()
        return ret_stop, ret_start