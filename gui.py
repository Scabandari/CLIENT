from tkinter import *
import ast
from utils import get_client_msg_num

# todo https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid#34277295

state = None
next_command = get_client_msg_num('toClient.txt')

CLIENT_MSG_NUMBER = get_client_msg_num('toClient.txt')

# types of incoming msg's from client
UPDATE_STATE = 'UPDATE-STATE'
RETURN_MSG = 'RETURN-MSG'
UPDATE_HIGH = 'UPDATE_HIGH'
UPDATE_OVER = 'UPDATE_OVER'
UPDATE_SOLDTO = 'UPDATE_SOLDTO'
UPDATE_NOTSOLD = 'UPDATE_NOTSOLD'

# Types of msg's to be sent to server
REGISTER = 'REGISTER'
DE_REGISTER = 'DE-REGISTER'
OFFER = 'OFFER'
BID = 'BID'
HIGHEST = 'HIGHEST'
BID_OVER = 'BID_OVER'
WIN = 'WIN'
BID_SOLDTO = 'BID_SOLDTO'
BID_NOTSOLD = 'BID_NOTSOLD'

# Types of msg's being received from client app
OFFER_CONF = 'OFFER-CONF' # todo make sure all these are being handeled
OFFER_DENIED = 'OFFER-DENIED'

REGISTERED = 'REGISTERED'
UNREGISTERED = 'UNREGISTERED'
DEREG_CONF = 'DEREG-CONF'
DEREG_DENIED = 'DEREG-DENIED'

BID = 'BID'
HIGHEST = 'HIGHEST'
WIN = 'WIN'
BID_OVER = 'BID-OVER'
SOLD_TO = 'SOLD-TO'
NOT_SOLD = 'NOT-SOLD'

SERVER_CRASHED = 'SERVER-CRASHED'



# offer_msgs = [OFFER_CONF, OFFER_DENIED]
# registration_msgs = [REGISTERED, UNREGISTERED, DEREG_DENIED, DEREG_CONF]
# bidding_msgs = [HIGHEST, WIN, BID_OVER, SOLD_TO, NOT_SOLD]
# # For making bids

# Types of return msg's for BIDDING
# TODO WE NEED ALL TYPES

register_received = [REGISTERED,  # types of return msg's to display in msg box for Register
                     UNREGISTERED,
                     DEREG_CONF,
                     DEREG_DENIED]

offer_received = [OFFER_CONF,  # types of return msg's to display in msg box for Offer
                  OFFER_DENIED]


bid_received = [HIGHEST, WIN, BID_OVER, SOLD_TO, NOT_SOLD, UPDATE_HIGH, UPDATE_NOTSOLD, UPDATE_OVER, UPDATE_SOLDTO]  # types of return msg's to display in msg box for Bidding


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


def make_bid_client(event):
    msg = msg_for_client(BID)
    update_txt(BID, msg)


# todo ADD CASES FOR TCP MSG'S HERE, MAKE CORRESPONDING FUNCTION FOR BUTTON LIKE register_client(), deregister_client()
def msg_for_client(msg_type):
    """Passing msg's to CLIENT from gui"""
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
    elif msg_type == BID:
        msg = {
            'request': 0,
            'type': msg_type,
            'name': name_bidding.get(),
            'ip': ip_bidding.get(),
            'amount': amount.get(),
            'item #': item_number.get()
        }
    #elif tcp msg's make your own version of msg w/ needed values

    #Not sure if these are all needed, adding them all for now
    elif msg_type == BID:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': itemNum.get(),
            'amount': amount.get()
        }
    elif msg_type == HIGHEST:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': 0, #needs to be read from file
            'amount': 0 #needs to be read from file
        }
    elif msg_type == WIN:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': 0, #needs to be read from file
            'Name': 'Adam', #needs to be read from file
            'ip': '192.168.2.245', #needs to be read from file
            'port': 0, #needs to be read from file
            'amount': 0 #needs to be read from file

        }
    elif msg_type == BID_OVER:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': 0, #needs to be read from file
            'amount': 0 #needs to be read from file
        }
    elif msg_type == BID_SOLDTO:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': 0, #needs to be read from file
            'name': 'Adam', #needs to be read from file
            'ip': '192.168.2.245', #needs to be read from file
            'port': 0, #needs to be read from file
            'amount': 0, #needs to be read from file
        }
    elif msg_type == BID_NOTSOLD:
        msg = {
            'request': 0,
            'type': msg_type,
            'item #': 0, #needs to be read from file
            'reason': 'No bids' #needs to be read from file
        }
    return msg


def update_txt(msg_type, msg):
    """
    This function updates the text file that passes msg's to the CLIENT. Mainly the state of items for bid
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
    elif ret_msg['type'] in bid_received:
        return_msg_bidding.set(msg_)


def update_bids(server_crashed_msg=None):
    global state
    msg = "" if server_crashed_msg is None else server_crashed_msg
    for item in state:
        msg += "Item #: " + str(item['item #']) + "\n"
        msg += "Seller: " + item['seller'] + "\n"
        msg += "Description: " + item['description'] + "\n"
        msg += "Highest bid: " + str(item['highest bid'][0]) + ": " + str(item['highest bid'][1]) + "\n"
        msg += "Minimum bid: " + str(item['minimum bid']) + "\n"
        msg += "Open status: " + str(item['open status']) + "\n\n\n"
    msg_box_str.set(msg)


def read_state():
    """
    This is where we're getting return msg's from the CLIENT
    :return:
    """
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
                    elif line[1] == SERVER_CRASHED:
                        update_bids(line[2])
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
itemNum = StringVar()
amount = StringVar()

return_msg_offer = StringVar()

############# Make Bids
name_bidding = StringVar()
ip_bidding = StringVar()
amount = StringVar()
item_number = StringVar()

return_msg_bidding = StringVar()
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
# OFFERS
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
###############################################################################################################
# Make Bids
make_bid_frame = Frame(root, bg="green", width=500, height=500)
make_bid_frame.pack(side=BOTTOM, expand=1)

name_label_make_bid = Label(make_bid_frame, text="Name: ")
ip_label_make_bid = Label(make_bid_frame, text="IP address: ")
bid_amount_label = Label(make_bid_frame, text="Bid Amount: ")
item_number_label = Label(make_bid_frame, text="Item #: ")

name_label_make_bid.grid(row=0)
ip_label_make_bid.grid(row=1)
bid_amount_label.grid(row=2)
item_number_label.grid(row=3)

entry_name_make_bid = Entry(make_bid_frame, textvariable=name_bidding)
entry_ip_make_bid = Entry(make_bid_frame, textvariable=ip_bidding)
bid_amount = Entry(make_bid_frame, textvariable=amount)
item_number = Entry(make_bid_frame, textvariable=item_number)

entry_name_make_bid.grid(row=0, column=1)
entry_ip_make_bid.grid(row=1, column=1)
bid_amount.grid(row=2, column=1)
item_number.grid(row=3, column=1)

make_bid = Button(make_bid_frame, text="Make Bid", bg="green", fg="black")
make_bid.bind("<Button-1>", make_bid_client)  # <Button-1> == left mouse button
make_bid.grid(row=4)

msg_box_make_bid = Message(make_bid_frame, textvariable=return_msg_bidding)

msg_box_make_bid.grid(row=5)
#################################################################################################################
canvas = Canvas(root, borderwidth=0, background="#ffffff")
bid_items_frame = Frame(canvas, bg="blue")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4, 4), window=bid_items_frame, anchor="nw")

bid_items_label = Label(bid_items_frame, text="Bidding Items")
bid_items_label.pack(side=RIGHT, expand=1)

msg_box = Message(bid_items_frame, textvariable=msg_box_str)
msg_box.pack(side=LEFT, expand=1)

root.after(1000, read_state)
root.mainloop()  # makes sure the gui constantly displays on screen
