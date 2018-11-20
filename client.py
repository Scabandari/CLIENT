import socket
import ast
from utils import (get_registration,
                   get_unregistration,
                   dict_to_bytes,
                   get_offer,
                   update_txt,
                   show_all_messages,
                   get_port,
                   get_bid,
                   sendTCPMessage,
                   req_number,
                   msg_to_queue)
import threading
from time import sleep

"""Here I'm thinking we need 2 threads in addition to the main thread. One that constantly checks 
    a list to see if there are user msg's to be sent over UDP and then another thread doing same 
    for TCP. We now have a 3rd thread checking for incoming UDP messages. When user decides from main 
    thread to answer at terminal they want to register they'll give some info and we create a msg 
    and put into the list the UDP thread keeps checking."""

CLIENT_MSG_NUMBER = 0  # next number of incoming msg from gui to client
RETURN_MSG = 'RETURN-MSG'
UPDATE_STATE = 'UPDATE-STATE'
UPDATE_CLIENTS = 'UPDATE-CLIENTS'
ITEMPORT = 'ITEMPORT' 
current_port = 0
current_item = 0

udp_messages = []
udp_msg_lock = threading.Lock()
tcp_messages = []
tcp_msg_lock = threading.Lock()

tcp_messages_returned = []  # tcp msg's returned from server, todo need this?
tcp_ret_lock = threading.Lock()
terminal_lock = threading.Lock()
#HOST = "192.168.1.184"  # this would normally be different and particular to the host machine ie client
HOST = "192.168.0.107"
UDP_PORT = 5075  # Clients UDP port they are listening on
SERVER_IP = "192.168.0.107"
SERVER_UDP_PORT = 5024
SERVER = (SERVER_IP, SERVER_UDP_PORT)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_socket.bind((HOST, UDP_PORT))

tcp_ip = HOST  # won't usually, get tcp servers machines local ip address on LAN
tcp_server_port = 5002
MY_TCP_PORT = 5010  # For listening, the server needs to know which port we're listening on
# when sending msg's to all clients over TCP
#tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TCP_CLIENT_PORT = 5071  # the port the client is listening for responses on
# If we wanted to set the port the client would listen for responses on we'd bind it like so
# tcp_socket.bind((HOST, TCP_CLIENT_PORT))
#tcp_socket.connect((tcp_ip, tcp_server_port))


'''
def tcp_incoming():
    global current_port
    while True:
        msg_received = receiveTCPMessage()
        msg = ast.literal_eval(msg_received)
        with terminal_lock:
            print("Received tcp msg: " + str(msg))
        try:
            if msg['set port']:
                current 
'''
def tcp_outgoing():
    while True:
        if tcp_messages:
            with tcp_msg_lock:
                msg = tcp_messages.pop(0)
            sendTCPMessage(msg)
# def tcp_incoming():
#     global MY_TCP_PORT
#     while True:
#         msg_received = tcp_socket.recv(1024).decode('utf-8')
#         msg = ast.literal_eval(msg_received)
#         with terminal_lock:
#             print("Received tcp msg: " + str(msg))
#         try:
#             if msg['set port']:
#                 MY_TCP_PORT = msg['port']
#         except KeyError:
#             pass
#
#
# def tcp_outgoing():
#     while True:
#         if tcp_messages:  # msg's to send
#             with tcp_msg_lock:
#                 msg = tcp_messages.pop(0)
#             tcp_socket.send(msg)
#             return_msg = tcp_socket.recv(1024).decode('utf-8')
#             with terminal_lock:
#                 print("Received back tcp response: " + return_msg)

# todo WHY DOES THIS WORK IN get_user_command OPTION C BUT NOT IN IT'S OWN THREAD?
def gui_msg(udp_messages_, udp_msg_lock_, CLIENT_MSG_NUMBER_):
    # global CLIENT_MSG_NUMBER
    # global udp_msg_lock
    # global udp_messages
    """ Read the next last line of text from toClient.txt and if """
    # todo read the next line in toClient.txt and put the msg in the correct queue
    while True:
        with open('toClient.txt', 'r') as f:
            for line in f:  # line ===> (number, state_dict)
                try:
                    line = ast.literal_eval(line)
                    if int(line[0]) >= CLIENT_MSG_NUMBER_:
                        print("reading toClient.txt")
                        CLIENT_MSG_NUMBER_ += 1
                        msg_for_server = line[2]
                        msg_for_server['request'] = req_number()
                        send_bytes = dict_to_bytes(line[2])
                        with udp_msg_lock_:
                            udp_messages_.append(send_bytes)
                        # try:
                        #     send_bytes = dict_to_bytes(line[2])
                        #     with udp_msg_lock:
                        #         udp_messages.append(send_bytes)
                        # except UnboundLocalError:
                        #     pass
                        # msg_to_queue(udp_messages, udp_msg_lock, line[2])
                except SyntaxError:
                    print("Could not read line in toClient.txt")
                    pass


def udp_incoming():
    # there are times when the UDP server will send all connected clients a msg such as NEW-ITEM msg's
    while True:
        #print("udp_outgoing")
        message, addr = udp_socket.recvfrom(1024)
        message = message.decode('utf-8')
        msg_dict = ast.literal_eval(message)
        if msg_dict['type'] == UPDATE_CLIENTS:
            update_txt(UPDATE_STATE, msg_dict['items'])
            continue
        elif msg_dict['type'] == ITEMPORT:
            global current_port
            current_port = msg_dict['port']
            print(current_port)
        print("Received udp message: " + message)
        update_txt(RETURN_MSG, message)


def udp_outgoing():
    while True:
        #print("udp_outgoing")
        if udp_messages:  # msg's to send
            with udp_msg_lock:
                msg = udp_messages.pop(0)
            udp_socket.sendto(msg, SERVER)
            # response, addr = udp_socket.recvfrom(1024)
            # response = response.decode('utf-8')
            # print("Receive back udp response: " + response)


gui_msg_reader = threading.Thread(target=gui_msg, args=(udp_messages, udp_msg_lock, CLIENT_MSG_NUMBER))
gui_msg_reader.start()

udp_incoming_thread = threading.Thread(target=udp_incoming)
udp_incoming_thread.start()

udp_outgoing_thread = threading.Thread(target=udp_outgoing)
udp_outgoing_thread.start()

# tcp_incoming_thread = threading.Thread(target=tcp_incoming)
# tcp_incoming_thread.start()

tcp_outgoing_thread = threading.Thread(target=tcp_outgoing)
tcp_outgoing_thread.start()

# gui_msg_reader = threading.Thread(target=gui_msg, args=(udp_messages, udp_msg_lock, CLIENT_MSG_NUMBER))
# gui_msg_reader.start()


def get_user_command():  # should be set on start up, include when sending TCP msg's
    """This function gives the user their options of different actions they can take
        and either returns None if their choice doesn't exist or the msg to be send
         over UDP to the server"""

    # todo the server should keep track of the request numbers so if the client initiates the contact how does it know
    # todo which request numbers are already taken or not???

    """
        Get a command from the user, determine if TCP or UDP msg will be sent and form msg
        then put in respective queue for dispatch by either TCP or UDP thread in client.py
    """
    choice = input("Enter a command: \n" +
                   "'r' ==> Registration and offers\n" +
                   "'b' ==> Bidding etc.\n" +
                   "'c' ==> Cancel, will free up terminal to display any responses from server\n::")
    if choice is 'r':
        selection = input("Enter a command: \n" +
                          "'r' ==> Registrations \n" +
                          "'of' ==> Offers:: \n")
        if selection == 'r':
            register_unregister = input("Enter a command: \n" +
                                        "'r' ==> Register to be able to offer or bid\n" +
                                        "'d' ==> De-register if you are already registered\n::")
            if register_unregister == 'r':
                send_msg = get_registration(MY_TCP_PORT)
            elif register_unregister == 'd':
                send_msg = get_unregistration()
            else:
                print("That option isn't available")
                return None
        elif selection == 'of':
            send_msg = get_offer()

        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass

    elif choice is 'b':
        """Before bidding for a given item, a registered client has to establish a TCP connection to
            the TCP socket associated with the item of interest at the server side. After this
            connection, a client can bid on the item by sending a BID message."""
        print("These are the items available:")
        # message to show all items
        send_msg = show_all_messages()
        # need to differentiate these two messages
        
        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass
        sleep(0.4)  # temp fix for display to allow udp incoming thread to run before the rest of the code runs
        send_msg = get_port()
        
        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass
        sleep(0.8)  # need to fix this
       
        send_msg = get_bid(HOST, current_port)

        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                tcp_messages.append(send_bytes)
        except UnboundLocalError:
            pass
    elif choice is 'c':
        return
        # gui_msg(udp_messages, udp_msg_lock, CLIENT_MSG_NUMBER)
    else:
        print("That option isn't available")
        return None


#########################################################################################
## FOR NOW YOU GUYS ARE USING THIS
# while True:
#     get_user_command()
##########################################################################################


########################################################################################
## ONCE GUI IS FINISHED WE USE THIS
udp_incoming_thread.join()

udp_outgoing_thread.join()

# tcp_incoming_thread.join()

tcp_outgoing_thread.join()

gui_msg_reader.join()
########################################################################################

