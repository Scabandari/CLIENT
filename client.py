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

tcp_messages_returned = []  # todo we need this?
tcp_ret_lock = threading.Lock()
terminal_lock = threading.Lock()
CHOICES = ['r']
HOST = "192.168.0.107"  # this would normally be different and particular to the host machine ie client
UDP_PORT = 5075  # UDP port
# todo check w/ prof that the server ip address will be known and don't need to get it programmatically
SERVER = ("192.168.0.107", 5024)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # todo need this? test pls
udp_socket.bind((HOST, UDP_PORT))

tcp_ip = HOST  # won't usually, get tcp servers machines local ip address on LAN
tcp_server_port = 5002
MY_TCP_PORT = None  # For listening, the server needs to know which port we're listening on
# when sending msg's to all clients over TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TCP_CLIENT_PORT = 5071  # the port the client is listening for responses on
# If we wanted to set the port the client would listen for responses on we'd bind it like so
# tcp_socket.bind((HOST, TCP_CLIENT_PORT))
tcp_socket.connect((tcp_ip, tcp_server_port))


def tcp_incoming():
    global MY_TCP_PORT
    while True:
        return_msg = tcp_socket.recv(1024).decode('utf-8')
        msg = ast.literal_eval(return_msg)
        with terminal_lock:
            print("Received tcp msg: " + return_msg)
        try:
            if msg['set port']:
                MY_TCP_PORT = msg['port']
        except KeyError:
            pass
        #print("type(msg): {}".format(type(msg)))


def tcp_outgoing():
    while True:
        # if tcp_messages_returned:
        #     with tcp_ret_lock:
        #         tcp_messages_returned.pop(0)
        #     print("Received back t")
        if tcp_messages:  # msg's to send
            with tcp_msg_lock:
                msg = tcp_messages.pop(0)
            tcp_socket.send(msg)
            #return_msg = tcp_socket.recv(1024).decode('ascii')
            return_msg = tcp_socket.recv(1024).decode('utf-8')
            with terminal_lock:
                print("Received back tcp response: " + return_msg)


# todo rename this
def udp_outgoing():
    while True:
        if udp_messages:  # msg's to send
            with udp_msg_lock:
                msg = udp_messages.pop(0)
            udp_socket.sendto(msg, SERVER)
            response, addr = udp_socket.recvfrom(1024)
            response = response.decode('utf-8')
            print("Receive back udp response: " + response)


udp_outgoing_thread = threading.Thread(target=udp_outgoing)
udp_outgoing_thread.start()

tcp_incoming_thread = threading.Thread(target=tcp_incoming)
tcp_incoming_thread.start()

tcp_outgoing_thread = threading.Thread(target=tcp_outgoing)
tcp_outgoing_thread.start()

while True:
    get_user_command(
        udp_messages,
        udp_msg_lock,
        tcp_messages,
        tcp_msg_lock,
        #tcp_messages_returned,
        tcp_ret_lock,
        terminal_lock,
        MY_TCP_PORT
    )




