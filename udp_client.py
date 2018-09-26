import socket
import ast
from utils import get_user_command

CHOICES = ['r']
HOST = "192.168.0.105"  # this would normally be different and particular to the host machine ie client
PORT = 5001
# todo check w/ prof that the server ip address will be known and don't need to get it programmatically
SERVER = ("192.168.0.105", 5000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # todo need this? test pls
s.bind((HOST, PORT))

command = get_user_command()
if command is not None:
    s.sendto(command, SERVER)
    response, addr = s.recvfrom(1024)
    response = response.decode('utf-8')
    print(response)




