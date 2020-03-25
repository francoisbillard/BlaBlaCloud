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
# Credit blablapookie@tartiflet.com

# ********** What now ? **********
#
# BS4, c'est vraiment par ce que je suis un flemmard, 
# et que j'aime bien cette lib

#####################################################################72


import requests
from bs4 import BeautifulSoup
from MyServerConfig import myServer, myLogin, myPassword

myHeaders = {
   'Accept_Language' : "fr-FR",
   "OCS-APIRequest" : "true"
   }

def main():
   global myServer, myLogin, myPassword
   talkURL = myServer + "/ocs/v2.php/apps/spreed/api/v1/"

   with requests.Session() as session:
      try:
         r = session.get(
            myServer, 
            auth = (myLogin, myPassword), 
            headers = myHeaders
            )
      except requests.exceptions.RequestException as e:
         raise SystemExit(e)
      
# Exemple de réccupération de la liste des conversations, 
# notez la grammaire : talkURL + "/room" particulièrement inélégante
      try:
         r = session.get(
            talkURL + "/room",
            headers = myHeaders
            )
      except requests.exceptions.RequestException as e:
         raise SystemExit(e)
      soup = BeautifulSoup(
         r.content,
         'html.parser'
         )
#      print(soup.prettify())

# Ici on va parcourir les conversations jusqu'à en trouver une 
# en particulier. Chacune d'elle est un <element>
      for conversation in soup.find_all('element'):
         if(conversation.token.get_text() == "efr56pd7"):
# On essaie de trouver l'ID du dernier message de la conversation pour
# satisfaire le param replyTo (qui est optionnel)
            lastMessageID = conversation.lastmessage.id.get_text()
            print(lastMessageID)

# Envoi d'un message dans la conv de test
# En définitive le param replyTo est optionnel et le param 
# actorDisplayName est optionnel lorsqu'on est identifié
      try:
         myMessage = {
            'message' : 'Trop foo!',
#            'actorDisplayName' : 'myAwesomeNick',
#            'replyTo' : lastMessageID
            }
# Ici encore un bijou de la méthode alar-h
         r = session.post(
            talkURL + "/chat/efr56pd7",
            data = myMessage,
            headers = myHeaders
            )
      except requests.exceptions.RequestException as e:
         raise SystemExit(e)

if __name__ == '__main__':
    main()