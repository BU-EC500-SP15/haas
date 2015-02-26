"""
Presentation #1 demo.  Mimics a rHaaS user registering nodes.  These nodes 
are placed in a local 'database'.  If a user requests a node outside the project
bHaaS registers a new one from the free pool.
"""

import sys
import urllib

import subprocess
from haas import cli
from haas import api
from haas import config
from haas.config import cfg
import json
import requests

#set up data collection
config.load()
config.configure_logging()


######This chunk is currently unused.  But it demonstrates that existing cli 
######code can be edited to help enable scripting 
def check_status_code(response):
    if response.status_code < 200 or response.status_code >= 300:
        sys.stderr.write('Unexpected status code: %d\n' % response.status_code)
        sys.stderr.write('Response text:\n')
        sys.stderr.write(response.text + "\n")
    else:
        return response.text
        #sys.stdout.write(response.text + "\n")

def object_url(*args):
    url = cfg.get('client', 'endpoint')
    for arg in args:
        url += '/' + urllib.quote(arg,'')
    return url

def do_get(url):
    return check_status_code(requests.get(url))

def list_free_nodes():
    """List all free nodes"""
    url = object_url('free_nodes')
    return do_get(url)
###########################################################################



def haas(*args):
    args = map(str, args)
    cmd = subprocess.check_output(['haas'] + args)
    return cmd

def parseString(output):
    parseable = []
    for i in output:
        parseable.append(i)
    
    parsedList = []
    element = ""
    textCapture = False
    for i in range(len(parseable)):
        if textCapture == True:
            if parseable[i] == "\"":
                parsedList.append(element)
                textCapture = False
                element = ""
            else:
                element += parseable[i]
        elif parseable[i] == "\"":
            textCapture = True
    return parsedList

def main():
    #free = list_free_nodes()
    #free.encode('ascii', 'ignore') #very possible to do it all this way took Ian's advice and change
    
    availableNodes = haas('list_project_nodes', 'img1')
    availableNodes = parseString(availableNodes)

    nodes = raw_input("What nodes would you like to add? ")
    node_list = nodes.split() #split the input into a list

    node_database = []
    
    for i in range(len(node_list)):
        if i == len(availableNodes):
            raw_input("Need to provision another node from bHaaS.  Continue?")
            haas('project_connect_node', 'img1', str(i))
            availableNodes = haas('list_project_nodes', 'img1')
            availableNodes = parseString(availableNodes)    
            node_database.append((node_list[i], availableNodes[i]))
        else:
            node_database.append((node_list[i], availableNodes[i]))
    
    raw_input("Want to see the database?")

    print node_database
 
main()