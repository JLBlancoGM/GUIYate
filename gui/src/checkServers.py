"""
Created on 15/05/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 01
SUMARY:  Checks if the servers are installed
"""
import const
import os
from logConfig import *

init_logger(const.LOG_FILE)


def checkserver():
    sip = 2*os.path.isdir(const.YATE)
    dhcp = 4*os.path.isdir(const.DHCP)
    ntp = 8*os.path.isdir(const.NTP)
    servers = sip + dhcp + ntp
    if servers == 0:
        return -1, 'Not servers installed'
        logging.error('Not servers installed, the program will be usable ')
    elif servers == 2:
        return 1, 'DHCP and NTP servers are not installed'
        logging.info('DHCP and NTP servers are not installed, the program will not has all functionality')
    elif servers == 4:
        logging.error('Not SIP server installed, the program will be usable ')
        return -1, 'SIP and NTP servers are not installed'
    elif servers == 6:
        logging.info('NTP server is not installed, the program will not has all functionality')
        return 1, 'NTP server is not installed'
    elif servers == 10:
        logging.info('DHCP server is not installed, the program will not has all functionality')
        return 1, 'DHCP server is not installed'
    elif servers == 12:
        logging.error('Not SIP server installed, the program will be usable ')
        return -1, 'Sip server is not installed'
    else:
        logging.info('All servers are installed')
        return 0