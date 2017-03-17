#slack api calls

from slackclient import SlackClient
import json

# create an instance of the api client and initialize it with a token
def init(token, privtoken):
    global api_client
    global priv_client
    api_client = SlackClient(token)
    priv_client = SlackClient(privtoken)
    return api_client

def getFullname(userid):
	return  json.loads(api_client.api_call('users.info', user=userid))['user']['profile']['real_name']

def getUsername(userid):
	return  json.loads(api_client.api_call('users.info', user=userid))['user']['name']

def sendRR(input):
	priv_client.api_call('chat.postMessage', channel='#announcements', text=input, as_user=False, username='torpbot', icon_emoji=':torpedo:')

def sendPM(input, userid):
	api_client.api_call('chat.postMessage', channel="@"+getUsername(userid), text=input, as_user=True)

def sendToChannel(input, channel):
	api_client.api_call('chat.postMessage', channel=channel, text=input, as_user=True)

def sendMessage():
	api_client.api_call('chat.postMessage', channel='#Testing', text='<http://google.com|test>', as_user=True)

def userInChannel(channel, user):
	channelInfo = json.loads(api_client.api_call('groups.info', channel=channel))

	if user in channelInfo['group']['members']:
		return True

	return False
	
	
