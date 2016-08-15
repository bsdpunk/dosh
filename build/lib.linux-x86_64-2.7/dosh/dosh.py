from __future__ import print_function
from datetime import datetime
import time
import ssl
import re
import readline
import threading
import sys
#import requests
import json
import os
from pprint import pprint
import signal,random, getpass
import urlparse, argparse
import pkg_resources
#Counters and Toggles
import readline
import codecs
import unicodedata
import rlcompleter
import random, shlex, atexit
import platform, time, calendar
import containers

arg_count = 0
no_auth = 0
database_count = 0
ddb_count = 0
hist_toggle = 0
prompt_r = 0


        
#For tab completion
COMMANDS = sorted(['containers'])

#For X number of arguements
ONE = ['containers']
TWO = ['containers']
THREE = ['nothing']
FOUR = ['domain-resource-create']
FIVE = ['domain-resource-create']
SIX = ['linode-disk-dist']
#For what class
RHSAT= ['sat-system-group-audit', 'sat-list-systems','sat-list-all-groups','sat-system-version','sat-list-users','sat-get-api-call','sat-get-version']
CONTAINER= ['containers']
HELPER = ['hidden','?','help', 'quit', 'exit','clear','ls', 'version', 'qotd']
UCOMMANDS = ['search-for-id','which','jump']
VMUTILS = ['esx-destroy-vm','esx-create-from-ova','esx-create-from-ovf','esx-vm-device-info', 'esx-perf-query', 'esx-list-datastores',  'esx-check-tools', 'esx-change-cd','esx-get-vm-uuid','esx-get-vm-name','esx-get-datastores','esx-get-resource-pools','esx-get-registered-vms','esx-get-hosts']
DOMAIN= ['domain-resource-create','list-domains','domain-resource-list']
SA = ['list-images','linode-list','linode-list-ip','linode-create', 'linode-shutdown','linode-disk-dist']
LU = ['avail-datacenters', 'avail-distributions', 'avail-plans', 'avail-stackscripts']
NB = ['nodebal-list', 'nodebal-node-list', 'nodebal-config-list', 'nodebal-create']

for arg in sys.argv:
    arg_count += 1

#warnings are ignored because of unverified ssl warnings which could ruin output for scripting
import warnings
warnings.filterwarnings("ignore")



#These are lists of things that are persistent throughout the session
username=''
details = {}
def complete(text, state):
        for cmd in COMMANDS:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1



#os expand must be used foR
config_file = os.path.expanduser('~/.dosh')
hist_file = os.path.expanduser('~/.trash_history')
buff = {}
hfile = open(hist_file, "a")
if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    username = raw_input("Username:")
    password = getpass.getpass("Password:")
    #vcenter = raw_input("VCenter Server (ex: company.local):")
    #sat_url =raw_input("Satellite Server Url (ex: https://redhat/rhn/rpc/api):")
    docker_ip =raw_input("Docker IP or Server uRL (EX: docker.local or 127.0.0.1):")
    #jump =raw_input("Jump Server(IP or DNS):")
    #linode_api_key = getpass.getpass("Linode-API-Key:")
    #api_key = linode_api_key 

    config= {"default":[{"username":username,"password":password, "docker-ip":docker_ip}]}
    
    config_file_new = open(config_file, "w")
    config_f = str(config)
    config_f = re.sub("'",'"',config_f)
    config_file_new.write(config_f)
    config_file_new.close 

#Ending when intercepting a Keyboard, Interrupt
def Exit_gracefully(signal, frame):
    #hfile.write(buff)
    sys.exit(0)



#DUH
def get_sat_key(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    #global username
    username = config["default"][0]["username"]
    password = config["default"][0]["password"]
    docker_ip = config["default"][0]["docker-ip"]
    #sat_url = config["default"][0]["sat_url"]
    #vcenter = config["default"][0]["vcenter"]
    #lkey = config["default"][0]["Linode-API-Key"]
    #api_key = config["default"][0]["Linode-API-Key"]
    key={}
    key['username']=username
    key['password']=password
    key['docker-ip']=docker_ip
    #key['platform']=ucommands.os_platform()
    #key['vcenter']=vcenter
    #key['si']=None
    #key['Linode-API-Key']=lkey
    #if sat_url:

        #if platform.python_version() == '2.6.6':
            #key['client'] = xmlrpclib.Server(sat_url, verbose=0)
        #else:
            #key['client'] = xmlrpclib.Server(sat_url, verbose=0,context=ssl._create_unverified_context())
        

        #key['key']=key["client"].auth.login(username, password)
    #else:
        #key['client'] = ''
    #key['jump'] = config["default"][0]["jump"]
    try:
        return(key)
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(key)

    

dosh_p = 'dosh '

#main command line stuff
def cli():
    while True:
        valid = 0

        signal.signal(signal.SIGINT, Exit_gracefully)
        try:
            if 'libedit' in readline.__doc__:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

            readline.set_completer(complete)
            readline.set_completer_delims(' ')
            cli = str(raw_input(PROMPT))
        except EOFError:
            bye()
        if hist_toggle == 1:
            hfile.write(cli + '\n')
        if 'key' in locals():
            pass
        else:
            key = get_sat_key(config)    

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario

#I miss perl :(


        cli = re.sub('  ',' ', cli.rstrip())
            



##########################################################################################
# This starts the single trash commands
#######################################################################################
        buff = str({calendar.timegm(time.gmtime()) : cli})
        #api_key = get_sat_key(config)
        #Write try statement here for error catching
        command = cli.split(' ', 1)[0]

        if command in CONTAINER:
            l_class = 'containers'
        elif command in LU:
            l_class = 'lin_utility'
        else:
            l_class = ''
        
        
        if len(cli.split(' ')) > 0:
            if len(cli.split(' ')) ==6:
                command,arg_one,arg_two,arg_three,arg_four,arg_five = cli.split()
                if command in SIX:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four,arg_five)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==5:
                command,arg_one,arg_two,arg_three,arg_four = cli.split()
                if command in FIVE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==4:
                command,arg_one,arg_two,arg_three = cli.split()
                if command in FOUR:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three)
                    print(result)
                    valid = 1

            if len(shlex.split(cli)) ==3:
                command,arg_one,arg_two = shlex.split(cli)
                if command in THREE:
                    command = command.replace("-", "_")
                    if l_class == 'vmutils':
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, si, arg_one, arg_two)
                    else:
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, arg_one, arg_two)
 
                    print(result)
                    valid = 1

            elif len(shlex.split(cli)) ==2:
                command,arguement = shlex.split(cli)
                if command in TWO:
                    command = command.replace("-", "_")
                    if l_class == 'vmutils':
                        api_key['vmarg'] = arguement
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, si)
                    else:
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, arguement)
                    
                    print(result)
                    valid = 1
                
                else:
                    print("Invalid Arguements")

            else:
               if cli in ONE:
                    cli = cli.replace("-", "_")
                    
                    if l_class == 'vmutils':
                        l_class = eval(l_class)
                        result = getattr(l_class, cli)(api_key, si)
                        pprint(result)
                        valid = 1
                    else:    
                        l_class = eval(l_class)
                        result = getattr(l_class, cli)(api_key)
                        pprint(result)
                        valid = 1
               elif cli in HELPER:
                    if cli == "quit" or cli == "exit":
                        #hfile.write(buff)
                        hfile.close()
                        bye()
                    if cli == "version":
                        print(version())
                        valid = 1
                    if cli == "hidden":
                        print(hidden_menu())
                        valid = 1
                    if cli == "ls":
                        print(ls_menu())
                        valid = 1
                    if cli == "qotd":
                        print(qotd_menu())
                        valid = 1
                    if (cli == "help") or (cli == "?"):
                        print(help_menu())
                        valid = 1
                    if cli == "clear":
                        if ucommands.os_platform() == 'windows':
                            print(os.system('cls'))
                            valid = 1
                        if ucommands.os_platform() == 'nix':
                            #pprint(
                            os.system('clear')
                            valid = 1
               else:
                    print("Invalid Command")

    

        if valid == 0:
            print("Unrecoginized Command")


def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
No Help currently Available

"""
    return(help_var)


def hidden_menu():
    hidden_var = """
No Hidden Commands Currently Available
"""
    return(hidden_var)



def version():
    version = pkg_resources.require("trash")[0].version
    return version

def bye():
    exit()

if arg_count == 2:
    command = sys.argv[1]
#noauth is essentially for testing
    if command == "noauth":
        no_auth = 1
#history is to toggle writing a history file, there is currently no clean up so it is off by default
    if command == "history":
        hist_toggle = 1
    if command == "roulette":
        rando = random.randint(1, 3)
    if command == "extra":
        trash_p = config["default"][0]["prompt"]

                 
PROMPT = dosh_p + '> '

if no_auth == 1:
    api_key =0
else:
    api_key = get_sat_key(config)


