from tkinter import *
import ast

# todo https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid#34277295
# ADJUST THE LAYOUT

root = Tk()  # creates a blank window

state = None
next_command = 1
msg_box_str = StringVar()
msg_box_str.set(state)


def update_bids():
    global state
    msg = ""
    for item in state:
        msg += "Seller: " + item['seller'] + "\n"
        msg += "Description: " + item['description'] + "\n"
        msg += "highest bid: " + str(item['highest bid'][0]) + ": " + str(item['highest bid'][1]) + "\n"
        msg += "minimum bid: " + str(item['minimum bid']) + "\n\n\n"
    msg_box_str.set(msg)


def read_state():
    global state
    with open('toGui.txt', 'r') as f:
        for line in f:                 # line ===> (number, state_dict)
            line = ast.literal_eval(line)
            if int(line[0]) >= next_command:
                state = line[1]
                # msg_box_txt.set(line[1])
                update_bids()
    root.after(2000, read_state)


def print_register(event):
    global msg_box_txt
    msg_box_txt.set("Goodbye cruel world")


name = StringVar()
ip = StringVar()
port = StringVar()

register_frame = Frame(root, bg="orange", width=500, height=500)
register_frame.pack(side=LEFT, expand=1)

name_label = Label(register_frame, text="Name: ")
ip_label = Label(register_frame, text="IP address: ")
port_label = Label(register_frame, text="Port #: ")

entry_name = Entry(register_frame, textvariable=name)
entry_ip = Entry(register_frame, textvariable=ip)
entry_port = Entry(register_frame, textvariable=port)

register = Button(register_frame, text="Register", bg="red", fg="black")
register.bind("<Button-1>", print_register)  # <Button-1> == left mouse button

name_label.grid(row=0, sticky=E)  # right aligned.. N,E,S,W
ip_label.grid(row=1)
port_label.grid(row=2)

entry_name.grid(row=0, column=1)
entry_ip.grid(row=1, column=1)
entry_port.grid(row=2, column=1)

bid_items_frame = Frame(root, bg="blue", width=500, height=500)
bid_items_frame.pack(side=RIGHT, expand=1)
bid_items_label = Label(bid_items_frame, text="Bidding Items")
bid_items_label.grid(row=0, column=0)

msg_box = Message(bid_items_frame, textvariable=msg_box_str)
msg_box.grid(row=1, column=2)


root.after(1000, read_state)
root.mainloop()  # makes sure the gui constantly displays on screen
