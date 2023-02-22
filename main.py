from requests_oauthlib import OAuth2Session
from pprint import pp
from requests_oauthlib import OAuth2Session
from flask import Flask, request
import os
import dotenv
from encryp import encrypt, decrypt
from database import insertData
import urllib.parse


dotenv.load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]



app = Flask(__name__)

temp = None
@app.route('/')
def index():

    code = request.args.get('code') #anilist auth will auto append this after user auths and open up this
    discordId = request.args.get('state')
    discordId = int(decrypt(discordId).decode())
    if not code:
        return "Code not provided"   
    elif not (discordId):
        return "Please sign in through discord. Contact kewb#7881 for inquiry"
    else:
        authUrl = f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={discordId}&response_type=code'

        oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
        authorization_url, state = oauth.authorization_url(authUrl)
        tokenUrl = 'https://anilist.co/api/v2/oauth/token'
        try:
            token = oauth.fetch_token(tokenUrl, code=code, client_secret=CLIENT_SECRET)
        except Exception as e:
            print(e)
            return "Something went wrong with the token, please contact kewb#7881 on discord"
        
        try:
            encrypted_token = encrypt(str(token))
        except Exception as e:
            print(e)
            return "An internal error occured with encryption"
        
        try:
            insertData(discordId=discordId, anilistToken=encrypted_token)
            return f"You can close this page and go back to Discord!"
        except Exception as e:
            print (e)
            return "An internal error occured with database"
    

def startWeb():
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

startWeb()

