from datetime import datetime
import base64
import socket
from dnslib import *
import time

class DNSServer:
    def __init__(self,port,ip):
        self.port = port
        self.ip = ip

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip,self.port))
        print("UDP Server Started Listening")
        while 1:
            req, address = sock.recvfrom(1024)
            printWithTime("UDP", f"Received {len(req)} bytes from {address}")
            request = DNSRecord.parse(req)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            qname = request.q.qname
            qn = str(qname)
            command = "echo hello"
            command_bytes = command.encode('ascii')
            base_64_bytes = base64.b64encode(command_bytes)
            resp = reply.pack()
            resp += b"\\" + base_64_bytes
            print(resp)
            time.sleep(2)
            sock.sendto(resp, address)

def printWithTime(head, message):
        curr_time = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{head}] [{curr_time[:-3]}]", message)

def main():
    dns = DNSServer(53,"127.0.0.1")
    dns.start()

main()