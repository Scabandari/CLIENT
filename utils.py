from random import randint
import json
#CHOICES = ['r', 'b']
REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'

# todo https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


# todo this possibly returns None, maybe change this
def get_user_command(
        udp_queue,
        udp_queue_lock,
        tcp_queue,
        tcp_queue_lock,
        #tcp_msg_return,
        tcp_ret_lock,
        terminal_lock,
        MY_TCP_PORT):  # should be set on start up, include when sending TCP msg's
    """This function gives the user their options of different actions they can take
        and either returns None if their choice doesn't exist or the msg to be send
         over UDP to the server"""
    # todo check if we've received a tcp msg in return, not sure yet if we even need this
    # with tcp_ret_lock:
    #     if tcp_msg_return:
    #         return_msg = tcp_msg_return.pop(0)
    #         print("Return msg: {}".format(return_msg))

    # todo the server should keep track of the request numbers so if the cient iniates the conact how does it know
    # which request numbers are already taken or not???
    request_number = randint(0, 100000)  # took a random in very large range to avoid probable conflicts

    # otherwise get a command from the user, determine if TCP or UDP msg will be sent and form msg
    # then put in respective queue for dispatch by either TCP or UDP thread in client.py
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
                # name = input("Enter your unique name identifier: ")
                # ip_address = input("Enter the ip address of the computer you'll be bidding from: ")
                # port = input("Enter the port number your computer will be listening on: ")
                name = 'ryan'
                ip_address = '192.168.0.107'
                port = 5000

                send_msg = {'request': request_number,
                            'type': REGISTER,
                            'name': name,
                            'ip': ip_address,
                            'port': MY_TCP_PORT}

            elif register_unregister == 'd':
                name = input("Enter the client name to de-register: ")
                ip = input("Enter the corresponding IP address for de-registration: ")
                send_msg = {
                    'request': request_number,
                    'type': 'DE-REGISTER',
                    'name': name,
                    'ip': ip
                }
            else:
                print("That option isn't available")
                return None

        if selection == 'of':
            # name = input("Enter your unique name identifier: ")
            # ip_address = input("Enter the ip address of your computer: ")
            # description = input("Enter a description of the item on offer: ")
            # min_bid = input("Enter the minimum bid: ")
            name = 'ryan'
            ip_address = '192.168.0.107'
            description = 'bat'
            min_bid = 10
            request_number = randint(0, 100000)

            send_msg = {'type': 'OFFER',
                        'request': request_number,
                        'name': name,
                        'ip': ip_address,
                        'description': description,
                        'minimum bid': min_bid}
            #send_bytes = dict_to_bytes(send_msg)
            # test_msg = "Successfully sent over tcp"
            # with tcp_queue_lock:
            #     tcp_queue.append(send_bytes)
            #     # tcp_queue.append(test_msg.encode('utf-8'))
        send_bytes = dict_to_bytes(send_msg)
        with udp_queue_lock:
            udp_queue.append(send_bytes)

    elif choice is 'b':
        pass
    elif choice is 'c':
        return
    else:
        print("That option isn't available")
        return None


def dict_to_bytes(dict_):
    json_str = json.dumps(dict_)
    bytes_ = json_str.encode('utf-8')  # todo: was ascii
    return bytes_