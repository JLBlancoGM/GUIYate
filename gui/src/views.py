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

def home(request):
    dicToResponse = {}
    update_users()
    dicToResponse.update(update_state())
    dicToResponse.update(update_users()[0])
    if request.method == 'POST':
        if 'start_sip' in request.POST:
            runserver = run_server('sip')
            if runserver[1]:
                dicToResponse['sip_error'] = runserver[0]
            dicToResponse.update(update_state())
        elif 'stop_sip' in request.POST:
            stop_server('sip')
            dicToResponse.update(update_state())
        if 'start_dhcp' in request.POST:
            runserver = run_server('dhcp')
            if runserver[1]:
                dicToResponse['dhcp_error'] = runserver[0]
            dicToResponse.update(update_state())
        elif 'stop_dhcp' in request.POST:
            stop_server('dhcp')
    return render_to_response('home.html', dicToResponse,
                              context_instance=RequestContext(request))


def update_state():
    dictionary = {}
    sip_server = ServerManager()
    dhcp_server = DHCPServer()
    if sip_server.is_start:
        dictionary['sip_server'] = 'Running'
        dictionary['sip_server_button'] = 'Stop'
        dictionary['sip_button'] = 'stop_sip'
    else:
        dictionary['sip_server'] = 'Stop'
        dictionary['sip_server_button'] = 'Start'
        dictionary['sip_button'] = 'start_sip'
    if dhcp_server.is_start:
        dictionary['dhcp_server'] = 'Running'
        dictionary['dhcp_server_button'] = 'Stop'
        dictionary['dhcp_button'] = 'stop_dhcp'
    else:
        dictionary['dhcp_server'] = 'Stop'
        dictionary['dhcp_server_button'] = 'Start'
        dictionary['dhcp_button'] = 'start_dhcp'
    return dictionary


def run_server(server):
    if server == 'sip':
        sip_server = ServerManager()
        start_sip = sip_server.run(0.5)
        if start_sip[1] == 0:
            return 'Server running', 0
        else:
            return 'Failure to run server. '+start_sip[0], 1
    if server == 'dhcp':
        dhcp_server = DHCPServer()
        start_dhcp = dhcp_server.run(0.5)
        if start_dhcp[1] == 0:
            return 'Server running', 0
        else:
            return 'Failure to run server.'+start_dhcp[0], 1


def stop_server(server):
    if server == 'sip':
        sip_server = ServerManager()
        if sip_server.stop()[1] == 0:
            return 'Server stopping'
        else:
            return 'Failure to stop server'


def update_users():
    dictionary = {}
    users = UserManager()
    if not users.table_ok:
        return dictionary, 1
    else:
        dictionary['users'] = users.list_users()
        return dictionary, 0