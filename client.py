import socket
import ast
from utils import get_user_command
import threading

"""Here I'm thinking we need 2 threads in addition to the main thread. One that constantly checks 
    a list to see if there are user msg's to be sent over UDP and then another thread doing same 
    for TCP. When user decides from main thread to answer at terminal they want to register they'll
     give some info and we create a msg and put into the list the UDP thread keeps checking."""

udp_messages = []
udp_msg_lock = threading.Lock()
tcp_messages = []
tcp_msg_lock = threading.Lock()
terminal_lock = threading.Lock()
CHOICES = ['r']
HOST = "192.168.0.107"  # this would normally be different and particular to the host machine ie client
PORT = 5075  # UDP port
# todo check w/ prof that the server ip address will be known and don't need to get it programmatically
SERVER = ("192.168.0.107", 5023)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # todo need this? test pls
udp_socket.bind((HOST, PORT))

tcp_ip = HOST  # won't usually, get tcp servers machines local ip address on LAN
tcp_port = 5001
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((tcp_ip, tcp_port))


def tcp_function():
    while True:
        if tcp_messages:
            with tcp_msg_lock:
                msg = tcp_messages.pop(0)
            tcp_socket.send(msg)
            return_msg = tcp_socket.recv(1024).decode('ascii')
            print("Received back tcp response: " + return_msg)


# todo rename this
def udp_function():
    while True:
        if udp_messages:
            with udp_msg_lock:
                msg = udp_messages.pop(0)
            udp_socket.sendto(msg, SERVER)
            response, addr = udp_socket.recvfrom(1024)
            response = response.decode('utf-8')
            print("Receive back udp response: " + response)


udp_thread = threading.Thread(target=udp_function)
udp_thread.start()

tcp_thread = threading.Thread(target=tcp_function)
tcp_thread.start()

while True:
    get_user_command(
        udp_messages,
        udp_msg_lock,
        tcp_messages,
        tcp_msg_lock
    )




