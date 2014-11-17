#!/usr/bin/env python 

import xmpp
import re
import getpass
import sys
from rsaenc import *
import base64

script = "<script type=\"text/javascript\">/* <![CDATA[ */(function(){try{var s,a,i,j,r,c,l,b=document.getElementsByTagName(\"script\");l=b[b.length-1].previousSibling;a=l.getAttribute('data-cfemail');if(a){s='';r=parseInt(a.substr(0,2),16);for(j=2;a.length-j;j+=2){c=parseInt(a.substr(j,2),16)^r;s+=String.fromCharCode(c);}s=document.createTextNode(s);l.parentNode.replaceChild(s,l);}}catch(e){}})();/* ]]> */</script>"

def get_dec_msg(msg):
    try:
        return decode(base64.b32decode(msg))
    except:
        return msg

def get_enc_msg(msg):
    try:
        return base64.b32encode(encode(msg))
    except:
        return msg


def message_handler(connect_object, message_node):
    if message_node.getBody() is not None:
        from_user = message_node.getFrom().getStripped()
        command = str(message_node.getBody())
        print m_roster.getName(from_user), ": ", get_dec_msg(command)
        message = get_enc_msg(raw_input())
        connect_object.send(xmpp.Message(message_node.getFrom(), message, typ='chat'))

# def myPresenceHandler(con, event):
#   fromjid = event.getFrom().getStripped()
#   # status = myroster.getStatus(fromjid)
#   print "handler", fromjid

# connect_object.send( xmpp.Message( message_node.getFrom() ,message, typ='chat'))
print "Enter username (example:abc@gmail.com): "
user = raw_input()
server = re.search('@(.+.com)', user).group(1)
user += script
# print "Enter password: "
password = getpass.getpass(stream=sys.stderr)
jid = xmpp.JID(user)
connection = xmpp.Client(server, debug=[])
connection.connect(server=('talk.google.com', 5223))
result = connection.auth(jid.getNode(), password, "sachin's-client")
if result:
    print "Authenticated and ready to go"
    connection.RegisterHandler('message', message_handler)
    # connection.RegisterHandler('presence', myPresenceHandler)
    m_roster = connection.getRoster()
    print "Online Contacts:"
    for roster in m_roster.getItems():
        if m_roster.getName(roster):
            print m_roster.getName(roster)
    print "-"*10, "Messages", "-"*10
    connection.sendInitPresence()
    while connection.Process(1):
        pass
else:
    print "Authentication failed"