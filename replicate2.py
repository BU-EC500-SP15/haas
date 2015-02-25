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

def main():
    #free = cli.list_free_nodes()    
    #data = cli.list_free_nodes()
    free = cli.list_free_nodes()
    print(free)

    #print(free)

main()