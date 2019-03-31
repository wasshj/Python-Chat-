


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def recevoir():
    """thread pour les messages arrivés."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: 
            break


def envoi(event=None):  
    """Envoi des messages."""
    msg = my_msg.get()
    my_msg.set("")  # Effacer text field.
    client_socket.send(bytes(msg, "utf8"))
    
    msg="moi: "+msg.split("//")[0]
    msg_list.insert(tkinter.END, msg)
       
        
    


def on_closing(event=None):
    client_socket.close()
    top.destroy()
    



top = tkinter.Tk()
top.title("MESSENGER ")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  
my_msg.set("Message...")
scrollbar = tkinter.Scrollbar(messages_frame)  

msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", envoi)
entry_field.pack()
send_button = tkinter.Button(top, text="Envoyer", command=envoi)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----La partie Socket----
HOST = input('Entrer nom de la hote: ')
PORT = input('Entrer le numero de port : ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

recevoir_thread = Thread(target=recevoir)
recevoir_thread.start()
tkinter.mainloop()  # Starts GUI execution.

