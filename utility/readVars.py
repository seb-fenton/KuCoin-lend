import json
import os

def readKeysFromEnv():
    
    key = os.environ.get("KC_KEY")
    secret = os.environ.get("KC_SECRET")
    passphrase = os.environ.get("KC_PASSPHRASE")

    return key, secret, passphrase