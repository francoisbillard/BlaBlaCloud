# BlaBlaCloud

What
====
De quoi faire parler tes scripts sur Nextcloud Talk.

Edites simplement le fichier MyServerConfig.py (sans trailing slash) avec les infos de ton instance Nextcloud.

Bisou.

Installation
=======


    > pip3 install -r requirements.txt
    > python3 setup.py install

Run
=

    > blablacloud -h
    Usage: blablacloud list -u <login> -p <pwd> -s <server>
           blablacloud send -u <login> -p <pwd> -s <server> <channel> <message> 
           blablacloud list -e 
           blablacloud send -e <channel> <message> 

    Command: 
        list    Get list of available channels
        send    Send a message to a channel
    
    Options:
        -u    username
        -p    password
        -s    server
    -e    use environnment variable : blablaserver, blablalogin, blablapwd
