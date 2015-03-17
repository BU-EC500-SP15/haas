"""
Un-register & delete the nodes set up by db_init.
Use to return to a state of no nodes registered.
"""
from subprocess import check_call
N_NODES=10
ipmiUser = "ADMIN_USER"
ipmiPass = "ADMIN_PASSWORD" 
def haas(*args):
    args = map(str, args)
    print args
    check_call(['haas'] + args)

for n in range(N_NODES):
    node = n
    ipmiIP = "10.0.0.0" + str(node+1)
    nic1_port = "R10SW1::GI1/0/%d" % (n)
    nic1 = 'nic1'
    haas('port_detach_nic', nic1_port)
    haas('port_delete', nic1_port)
    haas('node_delete_nic', node, nic1)
    haas('node_delete', node)
