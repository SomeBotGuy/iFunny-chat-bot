import sys
import json
import requests
import time
import websocket
from websocket import create_connection


class iFunnyBot:

    apiurl = "https://api.ifunny.mobi"
    app_id = "AFB3A55B-8275-4C1E-AEA8-309842798187"
    basicauth = "ODk5ODE4MDE0NTBBMDkzREE3NzlEQkVCMjA0RTkxNjRGRkYwRTk1NkUwREQ4MkYzNTgyOEM2RDJCOTZBMDJEQV9Nc09JSjM5UTI4OjdmMzVmNDc4OTRmMDNlYmYzMTNjNDFlMGRhZDg2YzQ4ZDY5M2FmNzc="
    myuid = ""
    mytoken = ""
    websoc = None

    def __init__(self, email=None, password=None):
        
        if email is not None and password is not None:
            self.login(email, password)

    def login(self, email, password):

        oauthurl = self.apiurl + "/v4/oauth2/token"

        daheader = {"Authorization":"Basic "+self.basicauth}

        paramz = {'grant_type':'password',
                   'username':email,
                   'password': password
                }
        req = requests.post(url = oauthurl, headers = daheader, data = paramz)

        if "invalid_grant" in req.text:

            print("Invalid login. Please check your credentials."+req.text)
            sys.exit(-1)
        
        elif "access_token" in req.text:
            gettoken = req.json()
            bearer = gettoken['access_token']

            print("bearer token "+bearer)

            self.getMessengerStuff(bearer)
            
        elif "too_many_user_auths" in req.text:
            print("Too many auths try logging in later or generate a new 'Basic' auth token if you do not want to wait")
            sys.exit(-1)

        else:
            print("Error could not log you in at this moment.")
            sys.exit(-1)

            
            
    def getMessengerStuff(self, token):

        myurl = self.apiurl + "/v4/account"

        daheader = {"Authorization":"Bearer "+token }

        req = requests.get(url = myurl, headers = daheader)

        mychat = req.json()

        chatuid = mychat['data']['id']
        chattoken = mychat['data']['messenger_token']

        self.myuid = chatuid
        self.mytoken = chattoken

        self.logintochat(chatuid, chattoken)



    def logintochat(self, uid, token):

        try:

            ws = create_connection("wss://ws-us-1.sendbird.com/?p=Android&pv=22&sv=3.0.55&ai=" + self.app_id + "&user_id="
                                    +uid + "&access_token=" + token)

            print("Bot is online!")

            self.setmsg(ws)


        except Exception as ex:
            print("Exception happened "+format(ex))



    def setmsg(self, ws):
        self.websoc = ws
        


    def getmsg(self):

        if self.websoc is not None:
            return self.websoc

        else:
            return None

    def sendmsg(self, channel, msg):
        jssend = json.dumps({'channel_url':channel,'message':msg},separators=(',', ':'))
        tosend = 'MESG{}\n'.format(jssend)
        self.websoc.send(tosend)

    def sendfile(self, channel, fileurl):


        mime = ""

        if fileurl.endswith(".jpg") or fileurl.endswith(".jpeg") or fileurl.endswith(".jpe"):
            mime = "image/jpeg"

        elif fileurl.endswith(".png"):
            mime = "image/png"
            
        elif fileurl.endswith(".bmp"):
            mime = "image/bmp"

        elif fileurl.endswith(".midi"):
            mime = "audio/midi"

        elif fileurl.endswith(".mpeg") or fileurl.endswith(".mp3") or fileurl.endswith(".mp4"):
            mime = "video/mpeg"

        elif fileurl.endswith(".oog"):
            mime = "video/oog"

        elif fileurl.endswith(".webm"):
            mime = "video/webm"

        elif fileurl.endswith(".wav"):
              mime = "audio/wav"

        else:
            print("Wrong file type")
            return

#MIME is commented out to help avoid blackhole image errors. if you experience errors with this uncomment it

        jssend = json.dumps({'channel_url':channel,'name':'botimage','req_id':str(int(round(time.time() * 1000))),
                                'thumbnails':[{'height':780,'width':780,'real_height':780,'real_width':780,
                                'url':fileurl}],#'type':mime,
                                 'url':fileurl},separators=(',', ':'))
        tosend = 'FILE{}\n'.format(jssend)
        self.websoc.send(tosend)


    def sendread(self, channel):
        jssend = json.dumps({'channel_url':channel},separators=(',', ':'))
        tosend = 'READ{}\n'.format(jssend)
        self.websoc.send(tosend)
        
            
