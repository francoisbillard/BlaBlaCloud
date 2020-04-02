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
        self.talk_url = os.path.join(server, Blablacloud.API_PATH)
        self.login = login
        self.password = password
        self.channels = []
        
        self.headers = {
            'Accept_Language' : "fr-FR",
            "OCS-APIRequest" : "true"
            }
        self.session = requests.session()
        try:
            self.session.get(
                self.server,
                auth=(self.login, self.password),
                headers=self.headers
                )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        self.init_channels()

    def init_channels(self):
        url = os.path.join(self.talk_url, "room")
        r = self.get_url(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        for conversation in soup.find_all('element'):
            self.channels.append((conversation.displayname.get_text().strip(), 
                                  conversation.token.get_text().strip()))
        
# Un simple Get 
    def get_url(self, url):
        try:
            result = self.session.get(url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

# Un simple Post
    def post(self, channel_name, payload):
        token = self.get_channels_token(channel_name)
        try:
            result = self.session.post(
            os.path.join(self.talk_url, "chat", token),
            data=payload,
            headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

    def get_channels_name(self):
        return [channel[0] for channel in self.channels]
    
# Renvoie le token du channel
    def get_channels_token(self, channel_name):
        all = [channel for channel in self.channels if channel[0] == channel_name]
        if not all:
            raise Exception("Channel not found")
        return [channel for channel in self.channels if channel[0] == channel_name][0][1]

