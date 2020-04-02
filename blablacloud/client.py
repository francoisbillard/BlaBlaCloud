'''
Created on 1 avr. 2020

@author: fb
'''

import os
import sys

from blablacloud.lib_blablacloud import Blablacloud
from docopt import docopt
from docopt import DocoptExit


class BlablaTalk:
    
    def __init__(self, server):
        self.server = server

    def connect(self, login, pwd):
        self.login = login
        self.pwd = pwd
        self.blaclacloud = Blablacloud(self.server, self.login, self.pwd)
        
    def sendMesgTo(self, channel_name, msg):
        self.blaclacloud.post(channel_name, {'message': msg})

    def getChannels(self):
        return self.blaclacloud.get_channels_name()

def main():

    usage = """
Usage: blablacloud list -u <login> -p <pwd> -s <server>
       blablacloud list -e 
       blablacloud send -e <channel> <message> 
       blablacloud send -e -i <channel> 
       blablacloud send -u <login> -p <pwd> -i -s <server> <channel> <message> 

Command: 
    list    Get list of available channels
    send    Send a message to a channel
    
Options:
    -u    username
    -p    password
    -s    server
    -e    use environnment variable : blablaserver, blablalogin, blablapwd
    -i    read message from stdin
"""
    try:
        args = docopt(doc=usage, argv=sys.argv[1:], help=True)
    except DocoptExit:
        raise

    login = args['<login>'] if args['-u'] else os.getenv("blablalogin", "login not set")
    pwd = args['<pwd>'] if args['-p'] else os.getenv("blablapwd", "pwd not set")
    server = args['<server>'] if args['-s'] else os.getenv("blablaserver", "server not set")

    
    blablatalk = BlablaTalk(server)
    blablatalk.connect(login, pwd)

    try:
        if args['send'] and not args['-i']:
            blablatalk.sendMesgTo(args['<channel>'], args['<message>'])
        if args['send'] and args['-i']:
            for line in sys.stdin:
                blablatalk.sendMesgTo(args['<channel>'], line)
    except Exception as e:
        print("Can not send message to %s (%s)" % (args['<channel>'], e))

    if args['list']:
        channels = blablatalk.getChannels()
        print("Channels : \n\t%s" % "\n\t".join(sorted(channels)))
