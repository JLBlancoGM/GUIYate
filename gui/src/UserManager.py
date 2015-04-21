"""
Created on 15/04/15

AUTHOR: Jose Luis Blanco
PROJECT: GUIYate
CONTACT: blancogmoreno@gmail.com
VERSION: 01
SUMARY: Clase para manejar los usuarios registrados
  en una base de datos mysql.
"""

import MySQLdb as db
import const
from logConfig import *


init_logger(const.LOG_FILE)

class UserManager(object):

    def __init__(self, hostdb, userdb, passdb, namedb):
        self.valuesdb = [hostdb, userdb, passdb, namedb]
        try:
            self.connectiondb = db.connect(*self.valuesdb)
        except db.OperationalError, err:
            msg_err = 'Connection refused ' + str(err)
            logging.error(msg_err)
            self.connect = False
        else:
            logging.info('Connection established')
            self.cursor = self.connectiondb.cursor()
            try:
                self.cursor.execute(const.USERS_TABLE)
            except db.OperationalError, err:
                if err[0] == 1050:
                    logging.info('Ok, the table users already exist')
                    self.table_ok = True
                else:
                    logging.info(' Error'+str(err))
                    self.table_ok = False
            except db.ProgrammingError, err:
                    logging.error(' Error'+str(err))
                    self.table_ok = False
            else:
                logging.info('Ok, table create')
                self.table_ok = True

    def reset_table(self):
        try:
            self.cursor.execute(const.RESET_TABLE)
        except db.ProgrammingError, err:
            logging.error('Error '+str(err))

    def add_user(self, name, password):
        values = "'" + name + "'" + " ," + "'" + password + "'," + " 1, NULL, NOW(), 'NULL')"
        mysql_msg = ' INSERT INTO users VALUES (' + values
        try:
            self.cursor.execute(mysql_msg)
        except db.IntegrityError, err:
            logging.error('Error ' + str(err))
            if err[0] == 1062:
                return -1, 'El usuario ' + name + ' ya existe'
            else:
                return -1, 'Error en la base de datos, mire en archivo de logs'
        else:
            self.connectiondb.commit()
            logging.info('Ok, add user')
            return 0, 'Usuario incorporado'

    def del_user(self, name):
        mysql_msg = "DELETE FROM users WHERE username = '%s' " % name
        rtn = self.cursor.execute(mysql_msg)
        self.connectiondb.commit()
        return rtn

    def list_users(self):
        mysql_msg = "SELECT username, inuse, location FROM users"
        self.cursor.execute(mysql_msg)
        data = self.cursor.fetchall()
        return data
