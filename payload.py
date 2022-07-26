import socket
import dns.name
import dns.message
import dns.query

class Payload:
    def __init__(self):
        pass

def payload(addr):
    query = dns.message.make_query("google.com", dns.rdatatype.A)
    result = dns.query.udp(query, addr, 5,ignore_trailing=True,ignore_unexpected=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 53))
    while 1:
        data, addr = sock.recvfrom(1024)
        print("received message: %s" % data)

payload("10.145.228.172")