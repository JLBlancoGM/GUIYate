"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""

LOG_FILE = '..'

#Data base data
DATABASE = ['localhost', 'root', 'radio88', 'yate']

#Data base methods
USERS_TABLE = (
    "CREATE TABLE users ("
    "username VARCHAR(128) UNIQUE"
    ", password VARCHAR(128)"
    ", inuse INTEGER"
    ", location VARCHAR(1024)"
    ", expires TIMESTAMP NULL DEFAULT NULL"
    ", type VARCHAR(20) NULL DEFAULT NULL) ")

RESET_TABLE = (
    "UPDATE users "
    "SET inuse = 0, location = NULL"
)

#SIP serverlocation
YATE = '/home/jose/Proyectos/TelefonicaVoIP/SIPUA/trunk'
SIP_FILE_CONF = YATE+'/conf.d/ysipchan.conf'

#DHCP servers location
DHCP = '/opt/dhcp-server'
DHCP_FILE_CONF = DHCP + '/etc/dhcpd.conf'

#NTP servers location
NTP = '/opt/ntp-server'


#PID files
PID_SIP_FILE = 'pid_sip'
PID_DHCP_FILE = 'pid_dhcp'
PID_NTP_FILE = 'pid_ntp'

#Default config lists
SIP_CONF_LIST = [('[general]', ''), ('type', 'UDP'), ('port', '5060'), ('useragent', 'SIPLAB'),
                  ('maxforwards', '20'), ('info', 'enable'), ('progress', 'disable'),
                  ('[registrar]', ''), ('expires_min', '60'), ('expires_def', '600'),
                 ('expires_max', '3600')]

DHCP_CONF_LIST = [('option domain-name', '"sheol.org"'), ('DHCPDARGS', 'wlan0'),
                  ('option domain-name-servers', ['ns1.example.org', 'ns2.example.org']),
                  ('option ntp-servers', '192.168.34.1'),
                  ('option sip-servers', '192.168.34.1'),
                  ('default-lease-time', '600'), ('max-lease-time', '7200'),
                  ('subnet', '192.168.34.0'), ('netmask', '255.255.255.0'),
                  ('range', '192.168.34.10'), ('range_end', '192.168.34.20'),
                  ('option routers', '192.168.34.1')]
