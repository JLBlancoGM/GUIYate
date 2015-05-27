"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""
from DHCPServer import DHCPServer
from ServerManager import ServerManager
from UserManager import UserManager
from CallToServer import CallToServer
from ConfigureDHCP import ConfigureDHCP
from ConfigureSIP import ConfigureSIP
from NTPServer import NTPServer
import const
import time
from checkServers import checkserver

def main():
    '''connect = UserManager('localhost', 'root', 'radio88', 'yate')
    connect.reset_table()
    print connect.list_users()'''
    server = ServerManager()
    if server.run()[1] == 0:
        call = CallToServer()
        #call.generic_comnand('status', ['\r\n', ])
        time.sleep(2)
        call.stop_remote()


def main2():
    dhcp = DHCPServer()
    dhcp.run()


def main3():
    dhcp_list_conf = const.DHCP_CONF_LIST
    dhcp_conf = ConfigureDHCP()
    dhcp_conf.set_conf(dhcp_list_conf)
    #conf = dhcp_conf.get_conf()
    #dhcp_conf.set_conf(conf)
    #print conf


def main4():
    print checkserver()

def main4():
    sip_conf_list = const.SIP_CONF_LIST
    sip_conf = ConfigureSIP()
    print " ", sip_conf.get_conf()

def main5():
    ntp = NTPServer()
    ntp.stop()
    ntp.run()
    time.sleep(10)
    ntp.restart()
    time.sleep(6)
    ntp.stop()

if __name__ == '__main__':
    main4()