"""
Created on 5/05/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 
SUMARY: Class to configure DHCP server
"""

import const
from logConfig import *


init_logger(const.LOG_FILE)


class ConfigureDHCP(object):
    def __init__(self):
        self.file_conf = const.DHCP_FILE_CONF

    def get_conf(self):
        configure = []
        try:
            with open(self.file_conf, 'r') as fl:
                for ln in fl:
                    ln = ln.split(' ')
                    if ln[0] == 'subnet':
                        line_conf2 = (ln[0], ln[1])
                        line_conf1 = (ln[2], ln[3])
                        configure.append(line_conf2)
                    elif ln[0] == '\trange':
                        line_conf2 = ('range', ln[1])
                        line_conf1 = ('range_end', ln[2].replace(';\n', ''))
                        configure.append(line_conf2)
                    elif ln[0] == '\toption':
                        if not ln[2] == 'routers':
                            line_conf1 = (ln[0].replace('\t', '') + ' ' + ln[1], ln[2].replace(';\n', ''))
                        else:
                            line_conf1 = (ln[0].replace('\t', '') + ln[1], ln[2].replace(';\n', ''))
                    elif ln[0] == 'option':
                        if ln[1] == 'domain-name':
                            line_conf1 = (ln[0] + ' ' + ln[1], ln[2].replace(';\n', ''))
                        elif ln[1] == 'domain-name-servers':
                            dns_tmp = [var.replace(',', '') for var in ln[2:len(ln)]]
                            dns = [var.replace(';\n', '') for var in dns_tmp]
                            line_conf1 = (ln[0] + ' ' + ln[1], dns)
                        elif ln[1] == 'ntp-servers':
                            ntp_tmp = [var.replace(',', '') for var in ln[2:len(ln)]]
                            ntp = [var.replace(';\n', '') for var in ntp_tmp]
                            line_conf1 = (ln[0] + ' ' + ln[1], ntp)
                        elif ln[1] == 'sip-servers':
                            line_conf1 = (ln[0] + ' ' + ln[1], ln[3].replace(';\n', ''))
                            print "[TRAZA] sip-servers", line_conf1
                    elif 'DHCPDARGS' in ln[0]:
                        values = ln[0].split('=')
                        line_conf1 = (values[0], values[1].replace(';\n', ''))
                    elif '}' in ln[0]:
                        line_conf1 = ('end', ln[0].replace('};\n', ''))
                    else:
                        if len(ln) > 1:
                            line_conf1 = (ln[0], ln[1].replace(';\n', ''))
                    configure.append(line_conf1)
        except IOError:
            logging.error('Can not read the dhcp configuration file')
        return configure

    def set_conf(self, list_conf):
        try:
            with open(self.file_conf, 'w') as fl:
                for key in list_conf:
                    if key[0] == 'subnet':
                        line = key[0] + ' ' + key[1]
                    elif key[0] == 'netmask':
                        line = ' ' + key[0] + ' ' + key[1] + ' {\n'
                    elif key[0] == 'range':
                        line = '\t' + key[0] + ' ' + key[1]
                    elif key[0] == 'range_end':
                        line = ' ' + key[1] + ';\n'
                    elif key[0] == 'DHCPDARGS':
                        if key[1] == '':
                            line = key[0] + '=eth0;\n'
                        else:
                            line = key[0] + '=' + key[1] + ';\n'
                    elif key[0] == 'option routers':
                        if not key[1] == '':
                            line = '\t' + key[0] + ' ' + key[1] + ';\n}'
                        else:
                            line = "\n}"
                    elif key[0] == 'option domain-name-servers':
                        if not key[1] == '':
                            line = key[0] + ' '
                            first = True
                            for dns in key[1]:
                                if first:
                                    line = line + dns
                                    first = False
                                else:
                                    line = line + ', ' + dns
                            line = line + ';\n'
                    elif key[0] == 'option ntp-servers':
                        if not key[1] == '':
                            line = key[0] + ' '
                            first = True
                            for ntp in key[1]:
                                if first:
                                    line = line + ntp
                                    first = False
                                else:
                                    line = line + ', ' + ntp
                            line = line + ';\n'
                    elif key[0] == 'option sip-servers':
                        if not key[1] == '':
                            line = key[0] + ' 1 ' + key[1] + ';\n'
                    else:
                        line = key[0] + ' ' + key[1] + ';\n'
                    fl.write(line)
        except IOError:
            logging.error('Can not edit the dhcp configuration file')
        finally:
            fl.close()
        fl.close()