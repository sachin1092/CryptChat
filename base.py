#!/usr/bin/env python 

import xmpp

user = "testsearce123@gmail.com<script type=\"text/javascript\">/* <![CDATA[ */(function(){try{var s,a,i,j,r,c,l,b=document.getElementsByTagName(\"script\");l=b[b.length-1].previousSibling;a=l.getAttribute('data-cfemail');if(a){s='';r=parseInt(a.substr(0,2),16);for(j=2;a.length-j;j+=2){c=parseInt(a.substr(j,2),16)^r;s+=String.fromCharCode(c);}s=document.createTextNode(s);l.parentNode.replaceChild(s,l);}}catch(e){}})();/* ]]> */</script>"
password = "Searce@123"
server = "gmail.com"


def message_handler(connect_object, message_node):
    if message_node.getBody() is not None:
        from_user = message_node.getFrom().getStripped()
        command = str(message_node.getBody())
        print "message from: ", from_user, command
        message = "you sent: " + command
        connect_object.send(xmpp.Message(message_node.getFrom(), message, typ='chat'))

# connect_object.send( xmpp.Message( message_node.getFrom() ,message, typ='chat'))

jid = xmpp.JID(user)
connection = xmpp.Client(server, debug=[])
connection.connect()
result = connection.auth(jid.getNode(), password, "LFY-client")
connection.RegisterHandler('message', message_handler)

connection.sendInitPresence()

while connection.Process(1):
    pass