#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

# ********** What ? **********
#
# De quoi faire causer tes scripts dans des chans Nextcloud Talk

# ********** How ? **********
#
# PEP8 inspired : 
#   https://www.python.org/dev/peps/pep-0008/
# Licence GNU GPL v3.0 :
#   https://www.gnu.org/licenses/gpl.html
# Nextcloud API Doc : 
#   https://docs.nextcloud.com/server/18/developer_manual/client_apis/
# Nextcloud Talk API Doc : 
#   https://nextcloud-talk.readthedocs.io/en/latest/

# ********** Who's to blame ? **********
#
# Credit blablapookie@pasouf.com

# ********** What now ? **********
#
# BS4, c'est vraiment par ce que je suis un flemmard, 
# et que j'aime bien cette lib
# Utiliser les mots de passe d'application nextcloud pour éviter 
# d'avoir recours à des login/pass

#####################################################################72

import requests
from bs4 import BeautifulSoup
import os


class Blablacloud:

    API_PATH = "ocs/v2.php/apps/spreed/api/v1/"

    session = requests.session()

# L'initialiseur réalise aussi le login de la session
    def __init__ (self, server, login, password):
        self.server = server
        self.talkURL = server + Blablacloud.API_PATH
        self.login = login
        self.password = password
        self.headers = {
            'Accept_Language' : "fr-FR",
            "OCS-APIRequest" : "true"
            }
        self.session = requests.session()
        try:
            print("get session on '%s' with '%s/%s'" % (self.server, self.login, self.password))
            self.session.get(
                self.server,
                auth=(self.login, self.password),
                headers=self.headers
                )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

# Un simple Get 
    def get_url(self, url):
        print(url)
        try:
            result = self.session.get(
            url,
            headers=self.headers
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

# Un simple Post
    def post(self, channel, payload):
        try:
            result = self.session.post(
            self.API_PATH + "/chat/" + channel,
            data=payload,
            headers=self.headers
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

    def get_channels_name(self):
        channels = []
        myURL = os.path.join(self.server, Blablacloud.API_PATH,"room")
        r = self.get_url(myURL)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        for conversation in soup.find_all('element'):
            channels.append(conversation.displayname.get_text())
        return channels
    
# Renvoie un dictionnaire {"nom du chan" : "token"}
    def get_channels_token(self, channelName):
        myChanList = {}
        myURL = self.server + Blablacloud.API_PATH + "/room"
        r = self.get_url(myURL)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        for conversation in soup.find_all('element'):
            myChanList[
                conversation.displayname.get_text()
                ] = conversation.token.get_text()
      
        return(myChanList)

