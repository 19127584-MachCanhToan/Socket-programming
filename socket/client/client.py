import os
from tkinter import*
import tkinter
from tkinter import messagebox
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
SERVER_DATA_PATH = "server_data"    
CLIENT_DATA_PATH = "client_data"
login = False

HOST = "127.0.0.1"
PORT = 8191
BUFSIZ = 1024
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break
def send(event=None):
    """ Handles sending of messages. """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    temp_msg=msg
    temp=str(msg)
    if msg != "#quit":
        msg=msg.split(" ")
        cmd=msg[0]
        if cmd !="#upload":
            sock.send(bytes(temp, "utf8"))
        else:
            cmd1=msg[1]
            if cmd1 =="change_name":
                cmd2=msg[3]
                path=CLIENT_DATA_PATH+'/'+msg[2]
                with open(path,"r") as f:
                    text=f.read()
                filename = path.split("/")[-1]
                send_data = f"{cmd}@{cmd1}@{filename}@{cmd2}@{text}"
                sock.send(bytes(send_data, "utf8"))
            elif cmd1=="multi_files":
                numberoffiles=len(msg)-2
                for i in range(numberoffiles):
                    path=CLIENT_DATA_PATH+'/'+msg[i+2]
                    with open(path,"r") as f:
                        text=f.read()
                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{cmd1}@{filename}@{text}"
                    sock.send(bytes(send_data, "utf8"))

            else:
                root=tkinter.Tk()
                canvas1 = tkinter.Canvas(root, width = 300, height = 300)
                canvas1.pack()
                def Application():
                    MsgBox = tkinter.messagebox.askquestion ('Mã hóa file','Bạn có muốn mã hóa file?',icon = 'warning')
                    path=CLIENT_DATA_PATH+'/'+msg[1]
                    with open(path,"r") as f:
                        text=f.read()
                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{filename}@{text}@{MsgBox}"
                    sock.send(bytes(send_data, "utf8"))
                button1 = tkinter.Button (root, text='Mã hóa file',command=Application,bg='brown',fg='white')
                canvas1.create_window(150, 150, window=button1)
    else:
        msg=msg.split(" ")
        cmd=msg[0]
        if cmd == "#quit":
            sock.close()
            top.quit()
       

 

def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    my_msg.set("#quit")
    send()

def Hello(event=None):
    """ Function for smiley button action """
    my_msg.set("Hello")    
    send()

def Goodbye(event=None):
    """ Function for smiley button action """
    my_msg.set("Goodbye")   
    send()
def Upload(event=None):
    my_msg.set("Upload")
    send()

#login
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    sock.send(bytes("register","utf8"))
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    sock.send(bytes("login","utf8"))
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
    user = username_info + " " + password_info
    sock.send(bytes(user,"utf-8"))
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
 
# Implementing event on login button 
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    user = username1 + " " + password1
    sock.send(bytes(user,"utf8"))
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    check = sock.recv(BUFSIZ).decode("utf8")
    if check == "True":
        login_sucess()
    elif check == "False":
        password_not_recognised()
    elif check == "Wrong User":
        user_not_found()
    



    ##################################################
    #list_of_files = os.listdir()
    #############################################################
    #if username1 in list_of_files:
     #   file1 = open(username1, "r")
     #   verify = file1.read().splitlines()
     #   if password1 in verify:
     #       login_sucess()
 
      #  else:
      #      password_not_recognised()
 
    #else:
    #    user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
    login_screen.destroy()
    main_screen.destroy()
 
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    main_screen.mainloop()
 
 
main_account_screen()
top = tkinter.Tk()
top.title("Phòng chat nhóm")
messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set,foreground="white",background="black")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

button_label = tkinter.Label(top, text="Enter Message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="black",background="white")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
Hello_button = tkinter.Button(top, text="Hello", command=Hello)
Hello_button.pack()
Bye_button = tkinter.Button(top, text="Goodbye", command=Goodbye)
Bye_button.pack()
Upload_button=tkinter.Button(top, text="Upload", command=Upload)
Upload_button.pack()
quit_button = tkinter.Button(top, text="Quit", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
#sock.send(byte("hello"),"utf_8")
#login_thread = Thread(target = main_account_screen)
#login_thread.start()
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

