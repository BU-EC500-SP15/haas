'''
This script implements node discovery over a subnet, searching for live hosts.
It requires nmap, freely available in many repositories.  To implement,
provide a network prefix, as well as a gateway ip.  

This script does not have implications for recursive haas, but it is a handy tool for 
learning about a network topology in order to perform fast provisioning across a network's nodes.
'''

from subprocess import check_output, STDOUT
import re
import socket

NETWORK_PREFIX = '192.168.56'
GATEWAY_IP = '192.168.56.1'

def getMyIp(dest_tuple):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(dest_tuple)
    ip = s.getsockname()[0]
    s.close()
    return ip

def getAvailableIps():
    nmap_scan = ''
    dots = 0
    for i in NETWORK_PREFIX:
        if i == '.':
            dots+=1
    if len(NETWORK_PREFIX) == 0:
        nmap_scan = check_output(['nmap', '0.0.0.0/0'], stderr=STDOUT)
        regex = re.compile('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
        nmap_list = regex.findall(nmap_scan)
    elif dots == 2: 
        nmap_scan = check_output(['nmap', NETWORK_PREFIX + '.0/24'], stderr=STDOUT)
        regex = re.compile(NETWORK_PREFIX + '.\d{1,3}')
        nmap_list = regex.findall(nmap_scan)
    elif dots == 1:
        nmap_scan = check_output(['nmap', NETWORK_PREFIX + '.0.0/16'], stderr=STDOUT)
        regex = re.compile(NETWORK_PREFIX + '.\d{1,3}.\d{1,3}')
        nmap_list = regex.findall(nmap_scan)
    elif dots == 0:
        nmap_scan = check_output(['nmap', NETWORK_PREFIX + '.0.0.0/8'], stderr=STDOUT)
        regex = re.compile(NETWORK_PREFIX + '.\d{1,3}.\d{1,3}.\d{1,3}')
        nmap_list = regex.findall(nmap_scan)
    return nmap_list

def main():

    my_ip = getMyIp((GATEWAY_IP, 22))
    nmap_output = getAvailableIps()    

    available_ips = list(set(nmap_output))

    if my_ip in available_ips:
        available_ips.remove(my_ip)
    
    available_ips.remove(GATEWAY_IP)

    print available_ips

main()
