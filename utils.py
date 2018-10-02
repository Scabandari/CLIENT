from random import randint
import json
CHOICES = ['r', 'b']
REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'

# todo https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


# def send_udp_msg(msg, socket_, server):  # todo needs socket param?
#     msg = str.encode(msg)
#     socket_.sendto(msg, server)
#     response, addr = socket_.recvfrom(1024)
#     response = response.decode('utf-8')
#     print(response)
#
#
# def send_tcp_msg():
#     pass


# todo this possibly returns None, maybe change this
def get_user_command(udp_queue, udp_queue_lock, tcp_queue, tcp_queue_lock):
    """This function gives the user their options of different actions they can take
        and either returns None if their choice doesn't exist or the msg to be send
         over UDP to the server"""
    choice = input("Enter a command: \n" +
                   "'r' ==> Registration and Registration\n" +
                   "'b' ==> Bidding, putting items up for bid etc.\n" +
                   ":: ")
    if choice is CHOICES[0]:
        # todo make function to give user their registration options and send UDP msg
        # todo same for TCP
        name = input("Enter your unique name identifier: ")
        ip_address = input("Enter the ip address of the computer you'll be bidding from: ")
        port = input("Enter the port number your computer will be listening on: ")
        request_number = randint(0, 100000)
        send_msg = {'request': request_number,
                    'type': REGISTER,
                    'name': name,
                    'ip': ip_address,
                    'port': port}
        send_bytes = dict_to_bytes(send_msg)
        with udp_queue_lock:
            udp_queue.append(send_bytes)

    elif choice is CHOICES[1]:
        selection = input("Enter a command: \n" +
                          "'of' ==> Offer an item for auction\n::")
        if selection == 'of':
            # name = input("Enter your unique name identifier: ")
            # ip_address = input("Enter the ip address of your computer: ")
            # description = input("Enter a description of the item on offer: ")
            # min_bid = input("Enter the minimum bid: ")
            # request_number = randint(0, 100000)
            #
            # send_msg = {'type': 'OFFER',
            #             'request': request_number,
            #             'name': name,
            #             'ip': ip_address,
            #             'description': description,
            #             'minimum bid': min_bid}
            #send_bytes = dict_to_bytes(send_msg)
            test_msg = "Successfully sent over tcp"
            with tcp_queue_lock:
                #tcp_queue.append(send_bytes)
                tcp_queue.append(test_msg.encode('ascii'))

    else:
        print("That option isn't available")
        return None


def dict_to_bytes(dict_):
    json_str = json.dumps(dict_)
    bytes_ = json_str.encode('utf-8')  # todo: was ascii
    return bytes_