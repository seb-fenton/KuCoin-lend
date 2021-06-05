import requests
import os
import time
import base64
import hmac
import hashlib 
import json

from utility.readVars import readKeys


def getBalance(targetCurrency):
    """ Retrieve the total balance and available balance in target currency
        of the user (specified by keys).
    
    Keyword arguments:
    targetCurrency -- coin ticker (i.e. BTC, USDT) to get user's balance
    """

    baseURL = 'https://api.kucoin.com/api/v1/accounts'

    apiKey, apiSecret, apiPassphrase = readKeys()
    headers = generateHeadersAccount(apiKey, apiSecret, apiPassphrase)

    response = requests.get(baseURL, headers=headers)
    balance, available = scrapeResponse(response, targetCurrency)

    return balance, available

def generateHeadersAccount(apiKey, apiSecret, apiPassphrase):
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'

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

def scrapeResponse(response, targetCurrency):
    for currencyBlock in response.json()['data']:
        if currencyBlock['currency'] == targetCurrency and currencyBlock['type'] == 'main':
            balance = currencyBlock['balance']
            available = currencyBlock['available']
            return balance, available

    raise BaseException('Currency not found in account')


if __name__ == "__main__":
    print(getBalance("USDT"))