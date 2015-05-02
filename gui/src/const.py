"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""

LOG_FILE = '..'
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

YATE = '/home/jose/Proyectos/TelefonicaVoIP/SIPUA/trunk'
DHCP = '/opt/dhcp-server'