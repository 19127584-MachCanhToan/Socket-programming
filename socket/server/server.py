  
""" Script for TCP chat server - relays messages to all clients """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import hashlib
clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 8191
BUFSIZ = 1024
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)
SERVER_DATA_PATH = "server_data"	
CLIENT_DATA_PATH = "client_data"
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SOCK.accept()
        access = False
        while True:
            check = client.recv(BUFSIZ).decode("utf8")
            if check == "register":
                register(client,client_address)
            elif check == "login":
                while True:
                    flag = check_login(client,client_address)
                    if flag == True:
                        access = True
                        break
                if access == True:
                    break
                    

        print("%s:%s has connected." % client_address)
        client.send("Greetings from the ChatRoom! ".encode("utf8"))
        #client.send("Now type your name and press enter!".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()

def register(conn,addr):
    user = conn.recv(BUFSIZ).decode("utf8")
    temp = user.split()
    username = temp[0]
    password = temp[1]
    file = open(username,"w")
    file.write(username + "\n")
    file.write(password)
    file.close()

def check_login(conn,addr):
    user = conn.recv(BUFSIZ).decode("utf8")
    temp = user.split()
    username = temp[0]
    password = temp[1]
    list_of_files = os.listdir()
    if username in list_of_files:
        file1 = open(username, "r")
        verify = file1.read().splitlines()
        if password in verify:
            conn.send(bytes("True","utf8"))
            return True
        else:
            conn.send(bytes("False","utf8"))
            return False
    else:
        conn.send(bytes("Wrong User","utf8"))
        return False


def handle_client(conn, addr):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = conn.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        temp=str(msg)
        upload="#upload"
        if msg == bytes("Upload","utf8"):
        	conn.send(bytes("mời chọn file để upload","utf8"))
        	files = os.listdir(CLIENT_DATA_PATH)
        	if len(files) ==0:
        		conn.send(bytes("thư mục rỗng","utf8"))
        	else:
        		t=" , ".join(f for f in files)
        		conn.send(bytes(t,"utf8")) 

        elif upload in temp:
        	temp=temp.split("@")
        	filepath=temp[1]
        	if (filepath=="change_name"):
        		filepath=temp[3]
        		content=temp[4][0:len(temp[2])-1]
        		filedestinationpath = os.path.join(SERVER_DATA_PATH,filepath)
        		with open(filedestinationpath, "w") as f:
        	 		f.write(content)
        		conn.send(bytes("upload file %s thành công"% filedestinationpath,"utf8"))
        	elif (filepath=="multi_files"):
        		filepath=temp[2]
        		content=temp[3][0:len(temp[3])-1]
        		filedestinationpath = os.path.join(SERVER_DATA_PATH,filepath)
        		with open(filedestinationpath, "w") as f:
        	 		f.write(content)
        		conn.send(bytes("upload file %s thành công"% filedestinationpath,"utf8"))
        	else:
        		check=temp[3][0:len(temp[3])-1]
        		if (check=="no"):
        			content=temp[2][0:len(temp[2])-1]
        			filedestinationpath = os.path.join(SERVER_DATA_PATH,filepath)
        			with open(filedestinationpath, "w") as f:
        	 			f.write(content)
        			conn.send(bytes("upload file %s thành công và file không mã hóa"% filedestinationpath,"utf8"))
        		else:
        			content=temp[2][0:len(temp[2])-1]
        			result = hashlib.md5(content.encode("utf8"))
        			filedestinationpath = os.path.join(SERVER_DATA_PATH,filepath)
        			with open(filedestinationpath, "w") as f:
        	 			f.write(str(result.hexdigest()))
        			conn.send(bytes("upload file %s thành công và file đã mã hóa"% filedestinationpath,"utf8"))	
        	
        elif msg != bytes("#quit", "utf8"):
        		broadcast(msg, name + ": ")
        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5)  # Listens for 5 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()
