import random
import requests
import socket
import string

def get_active_local_ip():
    # Get active local IP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tcp_socket.connect(('www.privateinternetaccess.com', 0))
        return tcp_socket.getsockname()[0]
    finally:
        tcp_socket.close()

def generate_client_id():
    # Generate client ID
    return ''.join( random.choice(string.hexdigits) for char in xrange(32) ).lower()

def acquire_port( user_name, password, client_id, local_ip, log ):
    # Set up parameters
    values = {'user':user_name,
              'pass':password,
              'client_id':client_id,
              'local_ip':local_ip}

    # Send request
    try:
        response = requests.post('https://www.privateinternetaccess.com/vpninfo/port_forward_assignment', params=values)
    except requests.exceptions.RequestException as request_exception:
        log( request_exception.message )
        return

    # Process response
    status_code_ok = 200
    if response.status_code != status_code_ok:
        log( '{}: '.format(response.status_code) + response.reason )
        return

    data = response.json()

    if 'port' not in data:
        log( data['error'] )
        return

    return data['port']
