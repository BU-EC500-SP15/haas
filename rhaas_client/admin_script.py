from __future__ import print_function
import ast

import sys
import fileinput
from subprocess import check_output

BHAAS_ENDPOINT = 'http://127.0.0.1:5000'
RHAAS_ENDPOINT = 'http://127.0.0.1:5001'

def haas(*args):
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

    bHaaS_output = haas('list_project_nodes', 'Test') #admin needs to know the name of the project in bHaas

    print("************")
    print("************")

    bHaaS_output = ast.literal_eval(bHaaS_output) #convert to list
    print('Here are node names in bHaaS:', bHaaS_output)
    print('This is how any you have:', len(bHaaS_output))

    changeEndpoint(RHAAS_ENDPOINT, BHAAS_ENDPOINT)

main()