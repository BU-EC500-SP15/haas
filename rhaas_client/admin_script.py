from __future__ import print_function

import sys

from subprocess import check_call, call

DELETE = sys.argv[0]

for arg in sys.argv:
    print(arg)

N_NODES=2
ipmiUser = "ADMIN_USER"
ipmiPass = "ADMIN_PASSWORD"

def haas(*args):
    #args = map(str, args)
    print (args)
    #check_call(['haas'] + args)
    #call(cmd)
    args = map(str, args)
    check_call(args)


def main():
    if DELETE == False:
        for n in range(N_NODES):
            node = n
            ipmiIP = "10.0.0.0" + str(node+1)
            nic1_port = "R10SW1::GI1/0/%d" % (n)
            nic1 = 'nic1'
            haas('node_register', node, ipmiIP, ipmiUser, ipmiPass)
            haas('node_register_nic', node, nic1, 'FillThisInLater')
            haas('port_register', nic1_port)
            haas('port_connect_nic', nic1_port, node, nic1)

    if DELETE == True:
        for n in range(N_NODES):
            node = n
            ipmiIP = "10.0.0.0" + str(node+1)
            nic1_port = "R10SW1::GI1/0/%d" % (n)
            nic1 = 'nic1'
            haas('port_detach_nic', nic1_port)
            haas('port_delete', nic1_port)
            haas('node_delete_nic', node, nic1)
            haas('node_delete', node)
    
    '''
    while True:
        #print('$: ', end='')
        line = sys.stdin.readline().strip()
        print(line)
        haas(line)
    '''

main()