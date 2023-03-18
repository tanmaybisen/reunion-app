import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str):
    return {
        "token": token
    }
    
def signJWT(res: list) -> Dict[str, str]:
    userdata=res[0]
    payload = {
        "userid" :  userdata.get('userid'),
        "username" :  userdata.get('username'),
        "email" :  userdata.get('email'),
        "expires": time.time() + 43200      # Logged in for 12 hours
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}