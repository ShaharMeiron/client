import socket
import os


root_dir = r"C:\Users\shahar\Desktop\projects\client\client_files"


def main():
    s = socket.socket()
    s.connect(("127.0.0.1", 1025))
    method = input("what do you want?  get post or exit : ")
    if method == "post":
        send_file(s)
    elif method == "get":
        get_file(s)


def get_file(s):
    name = input("which file would you want to get?")
    s.send(f"get\r\n{name}\r\n\r\n".encode())
    headers = recv_headers(s)
    print("file headers : ")
    print(type(headers))
    save_file(headers, s, name)


def save_file(headers, conn, name):
    print("saving file...")
    length = int(headers)
    print(headers)
    file_path = root_dir + f"\\{name}"
    con = conn.recv(length)
    f1 = open(file_path, 'wb')
    f1.write(con)
    f1.close()
    conn.send("file uploaded successfuly".encode())

        

def get_type(file_path): # gets the type of a file
    s = file_path.rfind(".")
    type = file_path[s + 1:]
    return type



def send_file(s): # send a kind of post request
    name = input("enter the file you'd like to post")
    path = root_dir + "\\path"
    f1 = open(path, 'rb')
    con = f1.read()
    f1.close()
    length = str(len(con))
    name = os.path.basename(path)
    headers = f"post\r\n{name}\r\n{length}\r\n\r\n"
    msg = headers.encode(encoding='utf-8') + con
    print("the msg:")
    print(msg)
    s.send(msg)
    print("sended")
    response = recv_till_end(s)
    print(f"server response: {response}")


def recv_till_end(s): # recv all data left
    data = ""
    ch = s.recv(1).decode()
    while ch:
        data += ch
        ch = s.recv(1).decode()
    return data


def show_response(s):
    response = ""
    ch = s.recv(1).decode()
    while ch:
        response += ch
        ch = s.recv(1).decode()
    print(response)


def recv_headers(conn):
    print("recieving headers...")
    headers = ""
    while headers[-4:] != "\r\n\r\n":
        headers += conn.recv(1).decode()
    return headers


main()

print("run have been complete")