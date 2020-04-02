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
        self.channel = self.blaclacloud.get_channels_name()[channel_name]
        self.blaclacloud.post(self.channel, {'message': msg})

    def getChannels(self):
        return self.blaclacloud.get_channels_name()

def main():

    usage = """
Usage: blablacloud list [-u <login>] [-p <pwd>] [-s <server>]  
       blablacloud send <channel> [-u <login>] [-p <pwd>] [-s <server>] message
       
Options:
    -u    username
    -p    password
    -s    server
"""
    try:
        args = docopt(doc=usage, argv=sys.argv[1:], help=True)
        print(args)
    except DocoptExit:
        raise
    
    blablatalk = BlablaTalk(args['<server>'])
    blablatalk.connect(args['<login>'], args['<pwd>'])

    if args['send']:
        blablatalk.sendMesgTo("testblablacloud", "hello")

    if args['list']: 
        print("Channels : \n\t%s" % "\n\t".join(blablatalk.getChannels()))
