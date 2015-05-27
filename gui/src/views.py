"""
Created on 2/05/15

AUTHOR: Jose Luis Blanco
PROJECT:  GUIYate 
CONTACT: blancogmoreno@gmail.com
VERSION: 01
SUMARY: Views.py. Python functions that take requests
        and returns a web response
"""

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from ServerManager import ServerManager
from DHCPServer import DHCPServer
from UserManager import UserManager
from ConfigureDHCP import ConfigureDHCP
from NTPServer import NTPServer
from ConfigureSIP import ConfigureSIP

import netifaces
import const
import os


def home(request):
    dicToResponse = {}
    if not check_root():
        dicToResponse['no_root'] = True
        dicToResponse.update(update_state('dhcp', False))
        dicToResponse.update(update_state('sip', False))
        dicToResponse.update(update_state('ntp', False))
        return render_to_response('home.html', dicToResponse,
                                  context_instance=RequestContext(request))
    dhcp = DHCPServer()
    sip = ServerManager()
    ntp = NTPServer()
    usersdb = UserManager()
    dicToResponse.update(update_state('dhcp', dhcp.is_start))
    dicToResponse.update(update_state('sip', sip.is_start))
    dicToResponse.update(update_state('ntp', ntp.is_start))
    dicToResponse.update(update_users(usersdb)[0])
    if request.method == 'POST':
        if 'start_sip' in request.POST:
            runserver = run_server(sip)
            if runserver[1] == 0:
                dicToResponse.update(update_state('sip', True))
            else:
                dicToResponse.update(update_state('sip', False))
                dicToResponse["server_error"] = runserver[0]
        elif 'stop_sip' in request.POST:
            stopserver = stop_server(sip)
            if stopserver[1] == 0:
                dicToResponse.update(update_state('sip', False))
            else:
                dicToResponse.update(update_state('sip', True))
                dicToResponse["server_error"] = stopserver[0]
        if 'start_dhcp' in request.POST:
            runserver = run_server(dhcp)
            if runserver[1] == 0:
                dicToResponse.update(update_state('dhcp', True))
            else:
                dicToResponse.update(update_state('dhcp', False))
                dicToResponse["server_error"] = runserver[0]
        elif 'stop_dhcp' in request.POST:
            stopserver = stop_server(dhcp)
            if stopserver[1] == 0:
                dicToResponse.update(update_state('dhcp', False))
                dicToResponse["server_error"] = stopserver[0]
            else:
                dicToResponse.update(update_state('dhcp', True))
                dicToResponse["server_error"] = stopserver[0]
        if 'start_ntp' in request.POST:
            runserver = run_server(ntp)
            if runserver[1] == 0:
                dicToResponse.update(update_state('ntp', True))
            else:
                dicToResponse.update(update_state('ntp', False))
                dicToResponse["server_error"] = runserver[0]
        elif 'stop_ntp' in request.POST:
            stopserver = stop_server(ntp)
            if stopserver[1] == 0:
                dicToResponse.update(update_state('ntp', False))
            else:
                dicToResponse.update(update_state('ntp', True))
                dicToResponse["server_error"] = stopserver[0]
        if 'add_user' in request.POST:
            if usersdb.connect and usersdb.table_ok:
                name = request.POST.get('user_name')
                passw = request.POST.get('user_pass')
                data_base_msg = usersdb.add_user(name, passw)
                if data_base_msg[0] == 0:
                    dicToResponse.update(update_users(usersdb)[0])
                else:
                    dicToResponse["add_user_fault"] = data_base_msg[1]
            else:
                    dicToResponse["add_user_fault"] = 'Database connection refused, read log file'
        if 'del_user' in request.POST:
            if usersdb.connect and usersdb.table_ok:
                name = request.POST.get('actual_user')
                dicToResponse.update(update_users(usersdb)[0])
    return render_to_response('home.html', dicToResponse,
                              context_instance=RequestContext(request))

def check_root():
    id = os.getuid()
    if id == 0:
        return True
    else:
        return False

def update_state(server, state):
    dictionary = {}
    if server == 'sip':
        if state:
            dictionary['sip_server'] = 'Running'
            dictionary['sip_server_button'] = 'Stop'
            dictionary['sip_button'] = 'stop_sip'
        else:
            dictionary['sip_server'] = 'Stop'
            dictionary['sip_server_button'] = 'Start'
            dictionary['sip_button'] = 'start_sip'
    if server == 'dhcp':
        if state:
            dictionary['dhcp_server'] = 'Running'
            dictionary['dhcp_server_button'] = 'Stop'
            dictionary['dhcp_button'] = 'stop_dhcp'
        else:
            dictionary['dhcp_server'] = 'Stop'
            dictionary['dhcp_server_button'] = 'Start'
            dictionary['dhcp_button'] = 'start_dhcp'
    if server == 'ntp':
        if state:
            dictionary['ntp_server'] = 'Running'
            dictionary['ntp_server_button'] = 'Stop'
            dictionary['ntp_button'] = 'stop_ntp'
        else:
            dictionary['ntp_server'] = 'Stop'
            dictionary['ntp_server_button'] = 'Start'
            dictionary['ntp_button'] = 'start_ntp'
    return dictionary


def run_server(server):
    return server.run(0.5)


def stop_server(server):
    return server.stop()


def update_users(users):
    dictionary = {}
    if not users.table_ok:
        return dictionary, 1
    else:
        dictionary['users'] = users.list_users()
        return dictionary, 0


def dhcpconf(request):
    dicToResponse = {}
    dicToResponse["interfaces"] = netifaces.interfaces()
    dhcp_conf = ConfigureDHCP()
    conf = dhcp_conf.get_conf()
    dicToResponse.update(update_dhcp(conf))
    if request.method == 'POST':
        index = request.POST.get('val_2')
        dicToResponse['index'] = index
        configuration = []
        for param, num in zip(const.DHCP_CONF_LIST, xrange(1, 13)):
            field = 'val_' + str(num)
            configure = request.POST.get(field)
            if param[0] == 'option domain-name':
                if not configure == '':
                    line = (param[0], '"'+configure+'"')
                    configuration.append(line)
            elif param[0] == "option domain-name-servers":
                value = configure.replace(' ', '')
                if not value == '':
                    line = (param[0], value.split(','))
                    configuration.append(line)
            elif param[0] == "option ntp-servers":
                value = configure.replace(' ', '')
                if not value == '':
                    line = (param[0], value.split(','))
                    configuration.append(line)
            elif param[0] == "option sip-servers":
                value = configure.replace(' ', '')
                if not value == '':
                    line = (param[0], value)
                    configuration.append(line)
            else:
                line = (param[0], configure)
                configuration.append(line)
        dhcp_conf.set_conf(configuration)
        conf = dhcp_conf.get_conf()
        dicToResponse.update(update_dhcp(conf))
    return render_to_response('dhcpconf.html', dicToResponse,
                              context_instance=RequestContext(request))


def update_dhcp(conf):
    dictionary = {}
    val = ''
    for value in conf:
        element = value[0].replace('option ', '')
        element = element.replace('-', '_')
        if element == 'domain_name':
            dictionary[element] = value[1].replace('"', '')
        elif element == 'domain_name_servers':
            for ls in value[1]:
                val = val + ls + ', '
            val = val[0:len(val)-2]
            dictionary[element] = val
        elif element == 'ntp_servers':
            val = ''
            for ls in value[1]:
                val = val + ls + ', '
            val = val[0:len(val)-2]
            dictionary[element] = val
        elif element == 'sip_servers':
            dictionary[element] = value[1]
        else:
            dictionary[element] = value[1]
    return dictionary


def sipconf(request):
    dicToResponse = {}
    sip = ConfigureSIP()
    conf_list = sip.get_conf()
    dicToResponse.update(update_select(conf_list))
    if request.method == 'POST':
        configure = []
        num = 1
        for param in const.SIP_CONF_LIST:
            if '[' in param[0][0]:
                value = (param[0], '')
            else:
                name = ('var_' + str(num))
                value = (param[0], request.POST.get(name).replace(' ', ''))
                num += 1
            configure.append(value)
        sip.set_conf(configure)
        conf_list = sip.get_conf()
        dicToResponse.update(update_select(conf_list))
    return render_to_response('sipconf.html', dicToResponse,
                              context_instance=RequestContext(request))


def update_select(conf_list):
    cont = 1
    dictionary = {}
    for value in conf_list[0]:
        if '[' in value[0]:
            pass
        else:
            value_pos = 'var_' + str(cont)
            val = value[1].replace('\n', '')
            val = val.replace(' ', '')
            if val == 'disable' or val == 'enable':
                dictionary[value[0].replace(' ', '')] = val
            elif val == 'UDP' or val == 'TCP':
                dictionary['type'] = val
            else:
                dictionary[value_pos] = value[1]
            cont += 1
    return dictionary
