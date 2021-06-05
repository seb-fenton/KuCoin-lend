import requests
import os
import time
import base64
import hmac
import hashlib 
import json

from getAccountStatus import getBalance
from getRates import getDailyLendingRate
from messageDiscord import sendMessage
from utility.readVars import readKeys

from dotenv import load_dotenv

def autoLend(currency):
    """ Auto-lend all available account equity at the most competitive 
        daily interest rate. 
    
    Keyword arguments:
    currency -- coin ticker (i.e. BTC, USDT) to get user's balance & find rate for
    """
    baseURL = 'https://api.kucoin.com/api/v1/margin/lend'

    balance, available = getBalance(currency)
    dailyIntRate = getDailyLendingRate(currency)

    key, secret, passphrase = readKeys()
    data = buildData(currency, dailyIntRate, int(float(available)))
    headers = generateHeadersLend(key, secret, passphrase, data)

    response = requests.post(baseURL, headers=headers, data=json.dumps(data))

    if json.loads(response.text)['code'] != "200000":
        sendMessage(f"Lend order failed with message: {response.text}")
    else:
        sendMessage(f"Order {response.text} succesful! Lent {available} USDT @ {dailyIntRate}%.")

def generateHeadersLend(apiKey, apiSecret, apiPassphrase, data):
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'POST' + '/api/v1/margin/lend' + json.dumps(data)

    signature = base64.b64encode(hmac.new(apiSecret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(apiSecret.encode('utf-8'), apiPassphrase.encode('utf-8'), hashlib.sha256).digest())

    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": apiKey,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": str(2),
        "Content-Type": "application/json"
    }
    return headers

def buildData(currency, dailyIntRate, size):
    # term is the 7-day lending period, which is the one we use due to market volatility
    return {'currency': currency, 'dailyIntRate': dailyIntRate, 'size': size, 'term': 7}


if __name__ == "__main__":
    load_dotenv()
    autoLend("USDT")