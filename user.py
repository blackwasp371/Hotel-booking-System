from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import socket
from plyer import notification    # if not installed, install it using `pip install plyer`

host = '127.0.0.1'
port = 5566

key = 13
characters = [' ', '.', '-', '(', ')', '!', '_', '>', '<', '/', '\\', '|', '+', '=', '[', ']', ':', ';', '`', '~', '"']

def encryption(message):
    encrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index + key) % 26 + ord('A')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index + key) % 26 + ord('a')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.isdigit():
            character_new = (int(character) + key) % 10
            encrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index + key) % len(characters)
            character_new = characters[character_shift]
            encrypted += character_new
        else:
            encrypted += character
    return encrypted

def decryption(message):
    dencrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index - key) % 26 + ord('A')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index - key) % 26 + ord('a')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.isdigit():
            character_new = (int(character) - key) % 10
            dencrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index - key) % len(characters)
            character_new = characters[character_shift]
            dencrypted += character_new
        else:
            dencrypted += character
    return dencrypted

def send_info(data):
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        messagebox.showerror("Error", str(e))
    ClientSocket.send(str.encode(data))
    Response = ClientSocket.recv(2048)
    response = decryption(Response.decode('utf-8'))
    if response == 'ACK':
        ClientSocket.close()
    elif response.startswith('DataInfo'):
        viewitem(response)
    elif response.startswith('Details has been added!'):
        notification.notify(title="Reservation Done", message="The requested reservation has been done!", app_name="Hotel Booking", timeout=10)
    elif response.startswith('Data Updated!'):
        notification.notify(title="Data Updated!", message="The data has been updated!", app_name="Hotel Booking", timeout=10)
    elif response.startswith('Data Deleted!'):
        notification.notify(title="Data Deleted!", message="The data has been deleted!", app_name="Hotel Booking", timeout=10)

def additem():
    e_1 = entry1.get()
    e_2 = entry2.get()
    e_3 = entry3.get()
    e_4 = entry4.get()
    e_5 = entry5.get()
    e_6 = entry6.get()

    if entry1.get() == "" and entry2.get() == "" and entry3.get() == "" and entry4.get() == "" and entry5.get() == "" and entry6.get() == "":

        messagebox.showerror("error", "all information must be filled")

    else:
        result = messagebox.askquestion("Submit",
                                          "You are about to enter following details\n" + e_1 + "\n" + e_2 + "\n" + e_3 + "\n" + e_4 + "\n" + e_5 + "\n" + e_6)
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        entry6.delete(0, END)
        # use of error handling try and except block
        try:
            if (result == "yes"):
                send_info(encryption(f"AddUser-|-{e_1}-|-{e_2}-|-{e_3}-|-{e_4}-|-{e_5}-|-{e_6}"))
            else:
                entry1.set("")
                entry2.set("")
                entry3.set("")
                entry4.set("")
                entry5.set("")
                entry6.set("")
        except:
            messagebox.showinfo("Info", "No information was added ")
    getitem()


def deleteitem():
    # tree.delete(*tree.get_children())
    e1 = entry1.get()
    e2 = entry2.get()
    e3 = entry3.get()
    e4 = entry4.get()
    e5 = entry5.get()
    e6 = entry6.get()
    if entry1.get() == "" and entry2.get() == "" and entry3.get() == "" and entry4.get() == "" and entry5.get() == "" and entry6.get() == "":
        messagebox.showerror("error", "there is issue with some information")
    else:
        result = messagebox.askquestion("Submit",
                                          "You are about to delete following details\n" + e1 + "\n" + e2 + "\n" + e3 + "\n" + e4 + "\n" + e5 + "\n" + e6)
        try:
            if (result == "yes"):
                send_info(encryption(f"Delete-|-{e1}-|-{e2}-|-{e3}-|-{e4}-|-{e5}-|-{e6}"))
            else:
                entry1.set("")
                entry2.set("")
                entry3.set("")
                entry4.set("")
                entry5.set("")
                entry6.set("")

        except:
            messagebox.showinfo("Info", "No information was deleted ")

        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        entry6.delete(0, END)
    getitem()

def updateitem():
    e1 = entry1.get()
    e2 = entry2.get()
    e3 = entry3.get()
    e4 = entry4.get()
    e5 = entry5.get()
    e6 = entry6.get()
    if entry1.get() == "" and entry2.get() == "" and entry3.get() == "" and entry4.get() == "" and entry5.get() == "" and entry6.get() == "":

        messagebox.showerror(
            "error", "sorry but there's some issue with this information..")
    else:
        result = messagebox.askquestion("Submit",
                                          "You are about to update following details\n" + e1 + "\n" + e2 + "\n" + e3 + "\n" + e4 + "\n" + e5 + "\n" + e6)

        if (result == "yes"):
            send_info(encryption(f"Update-|-{e1}-|-{e2}-|-{e3}-|-{e4}-|-{e5}-|-{e6}"))
            entry1.delete(0, END)
            entry2.delete(0, END)
            entry3.delete(0, END)
            entry4.delete(0, END)
            entry5.delete(0, END)
            entry6.delete(0, END)
    getitem()

def getitem():
    send_info(encryption("Get Data?"))

def viewitem(datas):
    tree.delete(*tree.get_children())
    items = datas.split('->')[1:]
    for item in items:
        dataum = item.split('-|-')
        tree.insert("", 0, values=(dataum[0], dataum[1],
                dataum[2], dataum[3], dataum[4], dataum[5]))
    txt_result.config(
        text="Successfully read the data from hotel.csv file", fg="black")

def selectItem(a):
    curItem = tree.focus()
    data = tree.item(curItem)["values"]
    try:
        entry1.insert(0, data[0])
        entry2.insert(0, data[1])
        entry3.insert(0, data[2])
        entry4.insert(0, data[3])
        entry5.insert(0, data[4])
        entry6.insert(0, data[5])
    except IndexError:
        clearitem()

def clearitem():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    root.title("Hotel Management System | Aakash Pun")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 996
    height = 557
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(0, 0)

    Name = StringVar()
    Address = StringVar()
    Phone_number = int()
    No_of_Guests = StringVar()
    Arrival_Date = StringVar()
    Departure_Date = StringVar()
    
    # raised is one of the styles of relief
    Top = Frame(root, width=900, height=50, bd=8, relief="raised")
    Top.pack(side=TOP)
    Left = Frame(root, width=200, height=500, bd=8, relief="raised")
    Left.pack(side=LEFT)
    Right = Frame(root, width=600, height=500, bd=8, relief="raised")
    Right.pack(side=RIGHT)
    Forms = Frame(Left, width=300, height=450)
    Forms.pack(side=TOP)
    Buttons = Frame(Left, width=300, height=250, bd=8, relief="raised")
    Buttons.pack(side=BOTTOM)
    
    txt_title = Label(Top, width=900, font=('arial', 24),
                  fg='#CC313D', text="Hotel Booking System")
    txt_title.pack()
    label0 = Label(Forms, text="Name:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label0.grid(row=0, stick="e")
    label1 = Label(Forms, text="Address:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label1.grid(row=1, stick="e")
    label2 = Label(Forms, text="Phone_number:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label2.grid(row=2, stick="e")
    label3 = Label(Forms, text="No.of Guests:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label3.grid(row=3, stick="e")
    label4 = Label(Forms, text="Arrival_Date:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label4.grid(row=4, stick="e")
    label5 = Label(Forms, text="Departure_Date:",
               fg='#CC313D', font=('arial', 16), bd=15)
    label5.grid(row=5, stick="e")
    txt_result = Label(Buttons)
    txt_result.pack(side=TOP)
    
    entry1 = Entry(Forms, textvariable=Name, width=30)
    entry1.grid(row=0, column=1)
    entry2 = Entry(Forms, textvariable=Address, width=30)
    entry2.grid(row=1, column=1)
    entry3 = Entry(Forms, textvariable=Phone_number, width=30)
    entry3.grid(row=2, column=1)
    entry4 = Entry(Forms, textvariable=No_of_Guests, width=30)
    entry4.grid(row=3, column=1)
    entry5 = Entry(Forms, textvariable=Arrival_Date, width=30)
    entry5.grid(row=4, column=1)
    entry6 = Entry(Forms, textvariable=Departure_Date, width=30)
    entry6.grid(row=5, column=1)
    
    btn_add = Button(Buttons, width=10, text="ADD", command=additem)
    btn_add.pack(side=LEFT)
    btn_delete = Button(Buttons, width=10, text="Delete", command=deleteitem)
    btn_delete.pack(side=LEFT)
    btn_update = Button(Buttons, width=10, text="UPDATE", command=updateitem)
    btn_update.pack(side=LEFT)
    btn_view = Button(Buttons, width=10, text="View", command=getitem)
    btn_view.pack(side=LEFT)
    btn_clear = Button(Buttons, width=10, text="CLEAR", command=clearitem)
    btn_clear.pack(side=LEFT)
    
    scrollbary = Scrollbar(Right, orient=VERTICAL)
    scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
    tree = ttk.Treeview(Right, columns=("Name", "Address", "Phone_number", "No. of Guests", "Arrival_Date", "Departure_Date"),
                    selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Phone_number', text="Phone_number", anchor=W)
    tree.heading('No. of Guests', text="No_of Guests", anchor=W)
    tree.heading('Arrival_Date', text="Arrival_Date", anchor=W)
    tree.heading('Departure_Date', text="Departure_Date", anchor=W)
    tree.bind('<ButtonRelease-1>', selectItem)
    tree.column('#0', stretch=NO, minwidth=20, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=80)
    tree.column('#2', stretch=NO, minwidth=0, width=80)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=80)
    
    tree.pack()
    
    root.mainloop()