import os
import socket
import threading
import csv

IP = "172.20.10.6"
PORT = 4457
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def handle_client(conn, addr):
    #check if conneciton established
    print("[NEW CONNECTION] {} connected.".format(addr))
    conn.send("OK@Client Connected.".encode(FORMAT))
    while True:
        #receive commands from client
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        
        #Upload file into server folder
        if cmd == "UPLD":
            text = data[1].split(',')
            print("test = ", [text])
            with open("webServer/CSV/database.csv", "a") as f:
                w = csv.writer(f, delimiter=',')
                w.writerow(text)

            conn.send("OK".encode(FORMAT))

        elif cmd == "QUIT":
            break

    print("[DISCONNECTED] {} disconnected".format(addr))
    conn.close()


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print("[LISTENING] Server is listening on {}:{}.".format(IP, PORT))

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        


if __name__ == "__main__":
    main()
