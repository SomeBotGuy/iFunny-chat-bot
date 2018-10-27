from iFunnyBot import iFunnyBot
import json
import time

email = "YOUR EMAIL HERE"
password = "YOUR PASSWORD HERE"

def run():
    
    ifbot = iFunnyBot(email, password)

    while True:

        websoc = ifbot.getmsg()


        if websoc is not None:

            try:

                inmsg = websoc.recv()

                

                othermsg = json.loads(inmsg[4:]) if inmsg != "" else "rip"

                if othermsg!="rip" and not inmsg.startswith('READ'):

                    if inmsg.startswith('MESG') and othermsg['user']['guest_id'] != ifbot.myuid:

                        print(othermsg['user']['name']+" says "+othermsg['message'])
                        ifbot.sendread(othermsg['channel_url'])
                        

                        if othermsg['message'] == "!hello":

                            ifbot.sendmsg(othermsg['channel_url'], "Hi, I'm online and responding!")


                        elif othermsg['message'] == "!image":
                            
                            ifbot.sendfile(othermsg['channel_url'], "https://vignette.wikia.nocookie.net/king-harkinian/images/4/47/Spongebob.png")


                    elif inmsg.startswith('FILE')and othermsg['user']['guest_id'] != ifbot.myuid:

                        print(othermsg['user']['name']+" sent a file\n"+othermsg['url'])

                    elif inmsg.startswith('BRDM'):

                        print("System message: "+othermsg['message'])

                    elif inmsg.startswith('EROR'):
                        print("Error "+othermsg['message'])

            except Exception as ex:

                if "already closed" in format(ex):
                    print("Reconnecting...")
                    ifbot.logintochat(ifbot.myuid, ifbot.mytoken)
                    continue

    


if __name__ == "__main__":
    try:
        run()
    except Exception as ex:
        print("Error "+format(ex))

