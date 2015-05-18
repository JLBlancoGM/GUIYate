"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""

LOG_FILE = '..'

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
DHCP_FILE_CONF = DHCP + '/etc/dhcp.conf'

#NTP servers location
NTP = '/opt/ntp-server'
NTP_FILE_CONF = NTP + '/etc/ntp.conf'

#PID files
PID_SIP_FILE = 'pid_sip'
PID_DHCP_FILE = 'pid_dhcp'


#Default config lists
SIP_CONF_LIST = [[('[general]', ''), ('type', 'UDP'), ('port', '5060'), ('useragent', 'SIPLAB'),
                 ('info', 'enable'), ], ]

DHCP_CONF_LIST = [('option domain-name', '"sheol.org"'),
                  ('option domain-name-servers', ['ns1.example.org', 'ns2.example.org']),
                  ('default-lease-time', '600'), ('max-lease-time', '7200'),
                  ('subnet', '10.5.5.0'), ('netmask', '255.255.255.224'),
                  ('range', '10.5.5.26'), ('range_end', '10.5.5.30'),
                  ('option routers', '10.5.5.1')]
