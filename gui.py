from tkinter import *
import ast

# todo https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid#34277295

state = None
next_command = 0

CLIENT_MSG_NUMBER = 0
# types of incoming msg's from client
UPDATE_STATE = 'UPDATE-STATE'
RETURN_MSG = 'RETURN-MSG'

# Types of msg's to be sent to server
REGISTER = 'REGISTER'
DE_REGISTER = 'DE-REGISTER'
OFFER = 'OFFER'

# Types of msg's being received from client app
OFFER_CONF = 'OFFER-CONF' # todo make sure all these are being handeled
OFFER_DENIED = 'OFFER-DENIED'
REGISTERED = 'REGISTERED'
UNREGISTERED = 'UNREGISTERED'
DEREG_CONF = 'DEREG-CONF'
DEREG_DENIED = 'DEREG-DENIED'

register_received = [REGISTERED,  # types of return msg's to display in msg box for Register
                     UNREGISTERED,
                     DEREG_CONF,
                     DEREG_DENIED]

offer_received = [OFFER_CONF,  # types of return msg's to display in msg box for Offer
                  OFFER_DENIED]
bid_received = []  # types of return msg's to display in msg box for Bidding


def register_client(event):
    """Take the fields for register, package a msg to send to client, pass to toClient.txt"""
    msg = msg_for_client(REGISTER)
    update_txt(REGISTER, msg)


def deregister_client(event):
    """Same as above but msg['type'] == DE_REGISTER"""
    msg = msg_for_client(DE_REGISTER)
    update_txt(DE_REGISTER, msg)


def offer_client(event):
    msg = msg_for_client(OFFER)
    update_txt(OFFER, msg)


# todo ADD CASES FOR TCP MSG'S HERE, MAKE CORRESPONDING FUNCTION FOR BUTTON LIKE register_client(), deregister_client()
def msg_for_client(msg_type):
    global name
    global ip
    global port

    msg = {}
    if msg_type == REGISTER:
        msg = {  # todo in client i have to set request and port
            'request': 0,
            'type': msg_type,
            'name': name.get(),
            'ip': ip.get(),
            'port': port.get()
        }
    elif msg_type == DE_REGISTER:
        msg = {  # todo in client i have to set request and port
            'request': 0,
            'type': msg_type,
            'name': name.get(),
            'ip': ip.get()
        }
    elif msg_type == OFFER:
        msg = {
            'request': 0,  # todo in client i have to set request and port
            'type': msg_type,
            'name': name_offer.get(),
            'ip': ip_offer.get(),
            'description': description.get(),
            'minimum bid': min_bid.get()
        }
    #elif tcp msg's make your own version of msg w/ needed values
    return msg


def update_txt(msg_type, msg):
    """
    This function updates the text file that passes msg's to the gui. Mainly the state of items for bid
    :param items:
    :return:
    """
    global CLIENT_MSG_NUMBER
    #client_tup = (CLIENT_MSG_NUMBER, msg_type, str(msg))
    client_tup = (CLIENT_MSG_NUMBER, msg_type, msg)
    CLIENT_MSG_NUMBER += 1
    with open('toClient.txt', 'a') as f:
        f.write(str(client_tup))
        f.write("\n")


def update_return_msg(msg_):
    global return_msg
    ret_msg = ast.literal_eval(msg_)
    if ret_msg['type'] in register_received:
        return_msg.set(msg_)
    elif ret_msg['type'] in offer_received:
        return_msg_offer.set(msg_)


def update_bids():
    global state
    msg = ""
    for item in state:
        msg += "Item #: " + str(item['item #']) + "\n"
        msg += "Seller: " + item['seller'] + "\n"
        msg += "Description: " + item['description'] + "\n"
        msg += "highest bid: " + str(item['highest bid'][0]) + ": " + str(item['highest bid'][1]) + "\n"
        msg += "minimum bid: " + str(item['minimum bid']) + "\n\n\n"
    msg_box_str.set(msg)


def read_state():
    global state
    global next_command
    try:
        with open('toGui.txt', 'r') as f:
            for line in f:                 # line ===> (number, state_dict)
                line = ast.literal_eval(line)
                if int(line[0]) >= next_command:
                    next_command += 1
                    if line[1] == UPDATE_STATE:
                        state = line[2]
                        update_bids()
                        # msg_box_txt.set(line[1])
                    elif line[1] == RETURN_MSG:
                        update_return_msg(line[2])
    except SyntaxError:
        pass

    root.after(2000, read_state)


# def print_register(event):
#     global msg_box_txt
#     msg_box_txt.set("Goodbye cruel world")


root = Tk()  # creates a blank window


msg_box_str = StringVar()
msg_box_str.set(state)
return_msg = StringVar()

######## Register
name = StringVar()
ip = StringVar()
port = StringVar()
###################

############# Offer
name_offer = StringVar()
ip_offer = StringVar()
description = StringVar()
min_bid = StringVar()

return_msg_offer = StringVar()
#########################################################################
register_frame = Frame(root, bg="orange", width=500, height=500)
register_frame.pack(side=LEFT, expand=1)

name_label = Label(register_frame, text="Name: ")
ip_label = Label(register_frame, text="IP address: ")
port_label = Label(register_frame, text="Port #: ")
latest_msg_label = Label(register_frame, text="LATEST MSG: ")

entry_name = Entry(register_frame, textvariable=name)
entry_ip = Entry(register_frame, textvariable=ip)
entry_port = Entry(register_frame, textvariable=port)

register = Button(register_frame, text="Register", bg="green", fg="black")
register.bind("<Button-1>", register_client)  # <Button-1> == left mouse button

de_register = Button(register_frame, text="De-register", bg="red", fg="black")
de_register.bind("<Button-1>", deregister_client)  # <Button-1> == left mouse button

return_msg_box = Message(register_frame, textvariable=return_msg)

name_label.grid(row=0, sticky=E)  # right aligned.. N,E,S,W
ip_label.grid(row=1)
port_label.grid(row=2)
register.grid(row=3)
de_register.grid(row=3, column=1)
latest_msg_label.grid(row=4)

entry_name.grid(row=0, column=1)
entry_ip.grid(row=1, column=1)
entry_port.grid(row=2, column=1)

return_msg_box.grid(row=5)
####################################################################################################################
offer_frame = Frame(root, bg="orange", width=500, height=500)
offer_frame.pack(side=BOTTOM, expand=1)

name_label_offer = Label(offer_frame, text="Name: ")
ip_label_offer = Label(offer_frame, text="IP address: ")
description_label = Label(offer_frame, text="Description: ")
min_bid_label = Label(offer_frame, text="Minimum bid: ")

name_label_offer.grid(row=0)
ip_label_offer.grid(row=1)
description_label.grid(row=2)
min_bid_label.grid(row=3)


entry_name = Entry(offer_frame, textvariable=name_offer)
entry_ip = Entry(offer_frame, textvariable=ip_offer)
entry_desc = Entry(offer_frame, textvariable=description)
entry_mindbid = Entry(offer_frame, textvariable=min_bid)

entry_name.grid(row=0, column=1)
entry_ip.grid(row=1, column=1)
entry_desc.grid(row=2, column=1)
entry_mindbid.grid(row=3, column=1)

offer = Button(offer_frame, text="Offer", bg="green", fg="black")
offer.bind("<Button-1>", offer_client)  # <Button-1> == left mouse button
offer.grid(row=4)

msg_box_offer = Message(offer_frame, textvariable=return_msg_offer)

msg_box_offer.grid(row=5)


# 'type': 'OFFER',
# 'request': req_number(),
# 'name': name,
# 'ip': ip_address,
# 'description': description,
# 'minimum bid': min_bid
#################################################################################################################
bid_items_frame = Frame(root, bg="blue", width=1000, height=500)
bid_items_frame.pack(side=RIGHT, expand=1)
bid_items_label = Label(bid_items_frame, text="Bidding Items")
bid_items_label.grid(row=0, column=0)

msg_box = Message(bid_items_frame, textvariable=msg_box_str)
msg_box.grid(row=1, column=2)


root.after(1000, read_state)
root.mainloop()  # makes sure the gui constantly displays on screen
