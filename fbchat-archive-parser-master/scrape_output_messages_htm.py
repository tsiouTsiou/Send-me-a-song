# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 14:50:33 2017

@author: MyCom
"""

import json
import os
from pprint import pprint
import re 

os.getcwd()
os.chdir("C:\\Users\\MyCom\\Desktop\\Projects\\Facebook Scraper\\fbchat-archive-parser-master") #TODO: should be given as user-input

data = json.loads(open('output.json', encoding="utf8").read().replace('\n', '')) # threads,user
#pprint(data)

noThreads = len(data['threads'])

USERNAME = "Linda de Voogd" #TODO: should be given from user
links = []

for i in range(0,noThreads):
    #print(data['threads'][i]['participants'][0])
    if (data['threads'][i]['participants'][0] == USERNAME):
        noMessages = len(data['threads'][i]['messages'])
        for j in range(0,noMessages):
            msg = data['threads'][i]['messages'][j]['message']
            if (re.match(".*https://www.youtube.com/watch.*",msg)):
                # example of link to be found
                links.append(re.search("https://www.youtube.com/watch\?v=[a-zA-Z_0-9-+_!@#$%^&*.,?]*",msg).group(0))
   
# TODO: to distinguish between sender/receiver             

# %%
# user authorization

# Sample Python code for user authorization

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret_213592566126-mgjqoorkua3ddrk4oen2sjt8982kk5bo.apps.googleusercontent.com.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
service = get_authenticated_service(args)

results = service.playlists().list(part='snippet,contentDetails',channelId="UCiMgZDqmyTD0UNL5nFc4PPw").execute()


