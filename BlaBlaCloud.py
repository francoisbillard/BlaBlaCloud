#!/usr/bin/env python3
#-*- coding:Utf-8 -*-

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
import MyServerConfig as MyConf

class Blablacloud:
    Session = requests.session()

# L'initialiseur réalise aussi le login de la session
    def __init__ (self, Server, Login, Password):
        self.Server = Server
        self.TalkURL = Server + MyConf.APIpath
        self.Login = Login
        self.Password = Password
        self.Headers = {
            'Accept_Language' : "fr-FR",
            "OCS-APIRequest" : "true"
            }
        self.Session = requests.session()
        try:
            self.Session.get(
                self.Server, 
                auth = (self.Login, self.Password), 
                headers = self.Headers
                )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

# Un simple Get 
    def GetURL(self,url):
        print(url)
        try:
         result = self.Session.get(
            url,
            headers = self.Headers
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

# Un simple Post
    def PostURL(self,url,payload):
        try:
         result = self.Session.post(
            url,
            data = payload,
            headers = self.Headers
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return(result)

# Renvoie un dictionnaire {"nom du chan" : "token"}
    def GetChanTokens(self):
        myChanList={}
        myURL = MyConf.APIpath + "/room"
        r = self.GetURL(myURL)
        soup = BeautifulSoup(r.content,'html.parser')
        for conversation in soup.find_all('element'):
            myChanList[
                conversation.displayname.get_text()
                ] = conversation.token.get_text()
        return(myChanList)

def main():
    b = Blablacloud(
        MyConf.Server, 
        MyConf.Login, 
        MyConf.Password
    )

# Exemple d'envoi de message dans le chan "le club des nerds"
    myChanToken = b.GetChanTokens()["Le club des nerds"]
    myURL = MyConf.APIpath + "/chat/" + myChanToken
    myMessage = "Message scripté"
    r = b.PostURL(myURL , {'message' : myMessage})

if __name__ == '__main__':
    main()
