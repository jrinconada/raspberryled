#!/usr/bin/python -t

import sys
import signal
import socket
import RPi.GPIO as GPIO

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.0.0.8', 1027))
    return s.getsockname()[0]

def usercancel(signal, frame):
    GPIO.cleanup()
    sys.exit();

HOST = ''
PORT = 8888
HOSTNAME = socket.gethostname()
MAX_REQUESTS = 5
BUFFER_SIZE = 1024
RESPONSE_HEADER = """\
HTTP/1.1 200 OK

"""

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
on = False

signal.signal(signal.SIGINT, usercancel)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(MAX_REQUESTS)

print 'Hostname: %s' % HOSTNAME
print 'IP: %s Port: %s' % (myip(), PORT)
print 'Listening...'

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(BUFFER_SIZE)
    print "Peticion recibida de %s" % client_address[0]

    response = RESPONSE_HEADER + "LED "
    on = not on
    if (on):
        response = response + "on"
    else:
        response = response + "off"

    client_connection.sendall(response)
    client_connection.close()

    GPIO.output(40, on)
