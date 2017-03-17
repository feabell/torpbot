import os, threading, sys, sqlite3

import slackapi
import yaml
import os
import logging
from time import gmtime, strftime

config = yaml.load(file('plugins/torp/torpbot.conf', 'r'))
token = config["SLACK_TOKEN"]
priv_token = config["SLACK_PRIV_TOKEN"]

api_client = slackapi.init(token, priv_token)

#logging.basicConfig(filename='/tmp/statsbot.log', level=logging.INFO)

outputs = []
crontable = []

fcChannelId = config["FC_TOKEN"]
announceChannelId = config["ANNOUNCE_TOKEN"]
botId = config['TORPBOT_ID']

logging.info('Torpbot started')

def process_message(data):
	#stop the bot from barfing out for events without a text, channel  or user chunk (event_ts chunks happen with unfurled links)
	if not 'text' in data:
		return
	if not 'user' in data:
		return
	if not 'channel' in data:
		return

	channel = data["channel"]
	user = data["user"]
	username = slackapi.getFullname(user)
    	text = data["text"].lower()
	textUncased = data["text"]
	#print data

	if channel == fcChannelId or (channel.startswith("D") and slackapi.userInChannel(fcChannelId, user)):
	  if text.startswith("!announce"):
	    blob = textUncased.split()

	    if len(blob) <2:
	      outputs.append([channel, "Not enough arguments supplied.  Include some text to announce"])
	      return

	    command = blob[0]
	    announce = ' '.join(blob[1:])

	    logging.info('announce command received from ' + username)

	    currtime = strftime('%H:%M %d-%m', gmtime())
	    message = 'Announcement by '+username+' at '+currtime+' (eve time):\r\n'+announce
  	    slackapi.sendRR(message)
	  
	

