"""
Register nodes with HaaS.
This is intended to be used as a template for either creating a mock HaaS setup
for development or to be modified to register real-life nodes that follow a
particular pattern.
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
	haas('node_register', node, ipmiIP, ipmiUser, ipmiPass)
	haas('node_register_nic', node, nic1, 'FillThisInLater')
	haas('port_register', nic1_port)
	haas('port_connect_nic', nic1_port, node, nic1)