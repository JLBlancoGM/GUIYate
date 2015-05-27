"""
Created on 13/05/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY:  
"""

import const
from logConfig import *


init_logger(const.LOG_FILE)


class ConfigureSIP(object):
    def __init__(self):
        self.config_files = (const.SIP_FILE_CONF,)

    def get_conf(self):
        configuration = []
        for flconf in self.config_files:
            try:
                with open(flconf, 'r') as fl:
                    configure = []
                    for line in fl:
                        if line[0] == ';':
                            continue
                        msg = line.split('=')
                        if msg[0][0] == '[':
                            configure.append(msg[0])
                        else:
                            if len(msg) == 1:
                                configure.append((msg[0], ''))
                            elif len(msg) > 1:
                                configure.append((msg[0], msg[1].replace(' ', '')))
                    configuration.append(configure)
            except IOError:
                logging.error('Can not read the sip configuration file')
        return configuration

    def set_conf(self, configuration):
        for flconf in self.config_files:
                try:
                    with open(flconf, 'w') as fl:
                        for line in configuration:
                                if '[' in line[0]:
                                    fl.write(line[0])
                                else:
                                    ln = line[0] + ' = ' + line[1]
                                    fl.write(ln)
                                fl.write('\n')
                except IOError:
                    logging.error('Can not read the sip configuration file')

