"""
This script keeps the number of nodes in the rHaaS free pool within a specified range.

Note that the current version does not do any authentication.  It assumes that rHaaS
is allowed to take free nodes as needed.

"""

from subprocess import check_output, STDOUT
from string import find, split
import json
import os

#PARAMETERS
MAX_FREE_NODES = 4;
MIN_FREE_NODES = 4;
BHAAS_ENDPOINT = 'http://127.0.0.1:5000'
RHAAS_ENDPOINT = 'http://127.0.0.1:5001'
ipmiUser = "ADMIN_USER"
ipmiPass = "ADMIN_PASSWORD"

# FIXME: Get project name from the .cfg file
# Trying to use cfg.get('recursive', 'project') throws a NoSectionError
# if running from r_client directory
b_project = 'BProj'

def haas(*args):
    args = map(str, args)
    return check_output(['haas'] + args, stderr=STDOUT, shell=False)

def changeEndpoint(new_endpoint):
    print "Changing to " + new_endpoint
    os.environ['HAAS_ENDPOINT'] = new_endpoint


def list_maker(str_output):   

        temp_str = str_output.replace('"', '')
        
        start = find(temp_str, '[')
        end = find(temp_str, ']')

        if ( end > (start + 1) ):
            list_output = split(temp_str[start+1:end], ', ') 
        else:
            list_output = [];

        return list_output

def add_node():
        
        #TODO: Handle case where bHaaS is out of free nodes

        changeEndpoint(BHAAS_ENDPOINT)
        print "Adding a node"
        
        bHaaS_output = haas('list_free_nodes')
        bHaaS_free_nodes = list_maker(bHaaS_output)

        print "bHaaS has %d availabile free nodes" %(len(bHaaS_free_nodes))

        free_info = haas('show_node', bHaaS_free_nodes[0])
    
        free_json = json.loads(free_info[find(free_info, '{') : ])

	print free_json 

        node = free_json['name']
        print 'Getting node: ' + node  
         
        haas('project_connect_node', b_project, node)
        
        changeEndpoint(RHAAS_ENDPOINT)

        nic = free_json['nics'][0]['label']
	
	macaddr = free_json['nics'][0]['macaddr']        

        # FIXME: these ipmiIP and nic_port formats are modeled on the dbinit.py script.
        # They are probably not universal.  In future, node could be a string that
        # can't be cast to an int. 

        ipmiIP = "10.0.0.0" + str( int(node) + 1 ) 
        nic_port = "R10SW1::GI1/0/" + node

        haas('node_register', node, ipmiIP, ipmiUser, ipmiPass)
        haas('node_register_nic', node, nic, macaddr)
        haas('port_register', nic_port)
        haas('port_connect_nic', nic_port, node, nic)

def delete_node(free_nodes):
        #The recursive node_delete takes care of reassigning the node
        #to the bHaaS free pool, so we don't have to deal with that here
        
        changeEndpoint(RHAAS_ENDPOINT)

        free_info = haas('show_node', free_nodes[0])
    
        free_json = json.loads(free_info[find(free_info, '{') : ])
        node = free_json['name']
 
        print 'Removing node: ' + node  
        
        nic = free_json['nics'][0]['label']
        
        haas('node_delete_nic', node, nic)
        haas('node_delete', node)


def main():

    call_output = haas('list_free_nodes')

    node_list = list_maker(call_output)

    n = len(node_list)

    print "rHaaS Free Nodes: "
    print node_list

    if (n < MIN_FREE_NODES):
        print "Too few nodes!"
        print "Adding %d more nodes to free pool..." %(MIN_FREE_NODES-n)  
        
        for i in range (MIN_FREE_NODES-n):
            add_node()

    elif (n > MAX_FREE_NODES):
        print "Too many nodes!"
        print "Returning %d nodes to base HaaS" %(n-MAX_FREE_NODES)
    
        for i in range (n-MAX_FREE_NODES):
            delete_node(node_list)

    else:
        print "Free pool within target range."

main()


