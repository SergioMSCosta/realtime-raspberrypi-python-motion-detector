# /home/shares/public/RaspberryPi/motion/code 
# python3 motion-alert.py

#!/usr/bin/python
# -*- coding: utf-8 -*-

import ortc

APP_KEY = 'YOUR_APP_KEY'
PVT_KEY = 'YOUR_PRIVATE_KEY'
AUTH_TOKEN = 'abcdefg'
CHANNEL = 'motion:cam1'
ORTC_URL = 'http://ortc-developers.realtime.co/server/2.1'

ortc_client = ortc.OrtcClient()

def on_exception(sender, exception):
    print ('ORTC Exception: ' + exception)

def on_connected(sender):
    print ('ORTC Connected')
    ortc_client.subscribe(CHANNEL, True, on_message)

def on_disconnected(sender):
    print ('ORTC Disconnected')
    import thread    
    thread.interrupt_main()

def on_message(sender, channel, message):
    print ('ORTC Message ('+channel+'): ' + message)
    ortc_client.unsubscribe(channel)
              
def on_subscribed(sender, channel):
    print ('ORTC Subscribed to: '+channel)
    ortc_client.send(channel, 'Seems like we have an intruder!')
        
def on_unsubscribed(sender, channel):
    print ('ORTC Unsubscribed from: '+channel)
    ortc_client.disconnect()

def on_reconnecting(sender):
    print ('ORTC Reconnecting')

def on_reconnected(sender):
    print ('ORTC Reconnected')

ortc_client.set_on_exception_callback(on_exception)
ortc_client.set_on_connected_callback(on_connected)
ortc_client.set_on_disconnected_callback(on_disconnected)
ortc_client.set_on_subscribed_callback(on_subscribed)
ortc_client.set_on_unsubscribed_callback(on_unsubscribed)
ortc_client.set_on_reconnecting_callback(on_reconnecting)
ortc_client.set_on_reconnected_callback(on_reconnected)

ortc_client.cluster_url = ORTC_URL
ortc_client.connect(APP_KEY)
ortc_client.disconnect()

try:
    while True:
        pass
except:
    pass
