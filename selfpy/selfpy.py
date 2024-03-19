import requests
from colorama import Fore
import websockets.client
import os
import atexit
import json
from .exceptions import *
import base64
token = None
headers = {}
def on_exit():
    print(Fore.RESET,"")
def login(token):
    global headers

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(Fore.RESET,"")
    print(Fore.BLUE,"""___ ___ _    ___ _____   __
 / __| __| |  | __| _ \ \ / /
 \__ \ _|| |__| _||  _/\ V / 
 |___/___|____|_(_)_|   |_|     0.0.1                
 """)
    print("")
    print(Fore.RED,"<!> selfpy's dev team is not reponsible for any damage <!>")
    token = token

    headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
    atexit.register(on_exit)
class settings():
    def change_status(text,status):
        '''Change status of a user account !
        
        Status : dnd,invisible,idle,online

        '''
        jsonData = {
            "status": status,
            "custom_status": {
                "text": text,

        }} 
        r = requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=jsonData)
        if r.status_code == 200:
            print(Fore.GREEN,"Status >> Sucessfully changed status !")
            return True
        elif r.status_code == 401:
            raise Invalid_Token("invalid_token")
            #raise requests.exceptions.ConnectionError("invalid_token")
        elif r.status_code == 429:
            raise ratelimit("ratelimit")
        elif r.status_code == 404:
            raise not_found("unknow")
    def change_profil_picture(path):
        try:
            payload = {
    "avatar": f"data:image/jpeg;base64,{base64.b64encode(open(path, 'rb').read()).decode()}"
}

            r = requests.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
            if r.status_code == 200:
                return True
            elif r.status_code == 401:
                raise Invalid_Token("invalid_token")
            elif r.status_code == 429:
                raise ratelimit("ratelimit")
            elif r.status_code == 404:
                raise not_found("unknow")
        except Exception as e:
            print(Fore.RED,f"selfpy >> Error while changing profile picture : {e}")
            return False

class messages():
    def typing(channel_id):
        '''Typing in a channel (channel id with "" !) (and very cool for trolling)'''
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/typing",headers=headers)
        if r.status_code == 204:
            return True
        elif r.status_code == 401:
            raise Invalid_Token("invalid_token")
        elif r.status_code == 429:
            raise ratelimit("ratelimit")
        elif r.status_code == 404:
            return {"status":"channel_not_found"}
    def send(text,channel_id):
        '''Send message to a channel (channel id with "" !, and return informations in json ! (Check docs) )'''

        json_data = {
            'content': text
        }

        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=json_data)
        print(r.text)
        
        if r.status_code == 200:
            print(Fore.GREEN,"Messages >> Sucessfully sended message ! !")
            i = json.loads(r.text)
            message_id = i["id"]

            return {"status":"true","id": message_id,"channel_id": channel_id}
        elif r.status_code == 401:
            raise Invalid_Token("invalid_token")
            #raise requests.exceptions.ConnectionError("invalid_token")
        elif r.status_code == 429:
            raise ratelimit("ratelimit")
        elif r.status_code == 404:
            return {"status":"channel_not_found"}
