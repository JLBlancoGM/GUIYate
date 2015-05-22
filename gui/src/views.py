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

import os


def home(request):
    dicToResponse = {}
    if not check_root():
        dicToResponse['no_root'] = True
        dicToResponse.update(update_state('dhcp', False))
        dicToResponse.update(update_state('sip', False))
        return render_to_response('home.html', dicToResponse,
                                  context_instance=RequestContext(request))
    dhcp = DHCPServer()
    sip = ServerManager()
    usersdb = UserManager()
    dicToResponse.update(update_state('dhcp', dhcp.is_start))
    dicToResponse.update(update_state('sip', sip.is_start))
    dicToResponse.update(update_users(usersdb)[0])
    if request.method == 'POST':
        if 'start_sip' in request.POST:
            runserver = run_server(sip)
            if runserver[1] == 0:
                dicToResponse.update(update_state('sip', True))
            else:
                dicToResponse.update(update_state('sip', False))
        elif 'stop_sip' in request.POST:
            stopserver = stop_server(sip)
            if stopserver[1] == 0:
                dicToResponse.update(update_state('sip', False))
            else:
                dicToResponse.update(update_state('sip', True))
        if 'start_dhcp' in request.POST:
            runserver = run_server(dhcp)
            if runserver[1] == 0:
                dicToResponse.update(update_state('dhcp', True))
            else:
                dicToResponse.update(update_state('dhcp', False))
        elif 'stop_dhcp' in request.POST:
            stopserver = stop_server(dhcp)
            if stopserver[1] == 0:
                dicToResponse.update(update_state('dhcp', False))
            else:
                dicToResponse.update(update_state('dhcp', True))
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
                print "[TRAZA] del user", usersdb.del_user(name)
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