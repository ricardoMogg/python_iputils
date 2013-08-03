import socket
import fcntl
import struct



def get_ip_address(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipaddr = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24]) 
    return ipaddr

def get_netmask(ifname='eth0'):
    return socket.inet_ntoa(fcntl.ioctl(
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM), 
        35099, 
        struct.pack('256s', ifname))[20:24])

def getInterface(interface="eth"):
    s = netifaces.interfaces()
    for n in s:
        if "eth" in n:
            return n    

def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def get_dns(dns_number="1"):
    counter = 0
    with open("/etc/resolv.conf") as f:
        content = f.readlines()
        for line in content:
            if "nameserver " in line:
                counter= counter+1
                if (str(counter) == dns_number):
                    return line[11:len(line)-1];


def replace(dns_1="None", dns_2="None"):  

    if(dns_1!="None" and dns_1!=""):
        if(dns_2 != "None" and dns_2 != ""):
            system("echo 'nameserver "+dns_1 +"\\nnameserver "+dns_2 +"'| sudo tee /etc/resolv.conf")
        else:
            system("echo 'nameserver "+dns_1 +"'| sudo tee /etc/resolv.conf")
    else:
        if(dns_2 != "None" and dns_2 != ""):
            system("echo 'nameserver "+dns_2 +"'| sudo tee /etc/resolv.conf")


