from __future__ import print_function

import sys
import fileinput
from haas import cli
from cStringIO import StringIO
from subprocess import check_call, call, check_output

DELETE = sys.argv[0]

ipmiUser = "ADMIN_USER"
ipmiPass = "ADMIN_PASSWORD"

BHAAS_ENDPOINT = 'http://127.0.0.1:5000'
RHAAS_ENDPOINT = 'http://127.0.0.1:5001'


def haas(*args):
    #print (args)
    args = map(str, args)
    return check_output(['haas'] + args)

def changeEndpoint(new_endpoint, old_endpoint):
    '''
    This function is not very stable.  Should be replaced by environmental variable
    '''
    for line in fileinput.input("haas.cfg", inplace=True):
        print(line.replace(old_endpoint, new_endpoint), end='')

def main():

    changeEndpoint(BHAAS_ENDPOINT, RHAAS_ENDPOINT)

    bHaaS_output = haas('list_project_nodes', 'Test')

    print("************")
    print(bHaaS_output)

    changeEndpoint(RHAAS_ENDPOINT, BHAAS_ENDPOINT)

main()