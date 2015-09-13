import httplib
import json
import random
import socket
import string
import urllib

PIA_SERVER = 'www.privateinternetaccess.com'

def get_active_local_ip():
    # Get active local IP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tcp_socket.connect((PIA_SERVER, 0))
        return tcp_socket.getsockname()[0]
    finally:
        tcp_socket.close()

def generate_client_id():
    # Generate client ID
    return ''.join( random.choice(string.hexdigits) for char in xrange(32) ).lower()

def acquire_port( user_name, password, client_id, local_ip, log ):
    # Set up parameters
    values = urllib.urlencode({'user':user_name,
                               'pass':password,
                               'client_id':client_id,
                               'local_ip':local_ip})

    # Send request
    connection = httplib.HTTPSConnection(PIA_SERVER)
    connection.request('POST', '/vpninfo/port_forward_assignment', values)
    response = connection.getresponse()

    # Process response
    status_code_ok = 200
    if response.status != status_code_ok:
        log( '{}: '.format(response.status) + response.reason )
        return

    # Extract port from json data
    data = json.load(response)

    if 'port' not in data:
        log( data['error'] )
        return

    return data['port']
