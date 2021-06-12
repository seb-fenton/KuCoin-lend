import requests
import os
import json
import math

import kuCoinInterface
import messageDiscord

from utility.readVars import readKeysFromEnv
from utility.buildHeaders import generateHeadersJson

def autoLend(currencyTicker = "USDT"):
    """ Auto-lend all available account equity for a given token
        at the most competitive daily interest rate. 
    """
    order = buildLendOrder(currencyTicker)
    sendLendOrder(order)

def buildLendOrder(currencyTicker):
    currencyAvailable, interestRate =  getKeyMetrics(currencyTicker)
    order = buildOrder(currencyTicker, currencyAvailable, interestRate)

    return order

def getKeyMetrics(currencyTicker):
    currencyAvailable = kuCoinInterface.getAvailable(currencyTicker)
    interestRate = kuCoinInterface.getDailyLendingRate(currencyTicker)

    return currencyAvailable, interestRate

def buildOrder(currencyTicker, currencyAvailable, interestRate):
    baseURL = getBaseURL()

    orderData = buildOrderData(currencyTicker, currencyAvailable, interestRate)
    headers = buildHeaderFromOrderData(orderData, baseURL)
        
    return baseURL, headers, orderData

def getBaseURL():
    return "https://api.kucoin.com/api/v1/margin/lend"

def buildOrderData(currencyTicker, currencyAvailable, interestRate):
    # we hardcode lendOrderLength here as the KuCoin API expects this specific value
    lendOrderLength = 7
    lendSize = math.floor(float(currencyAvailable))

    orderData = {'currency': currencyTicker,
                 'dailyIntRate': interestRate, 
                 'size': lendSize, 
                 'term': lendOrderLength}
    return orderData

def buildHeaderFromOrderData(orderData, baseURL):
    publicKey, secretKey, passphrase = readKeysFromEnv()
    headers = generateHeadersJson(publicKey, secretKey, passphrase, orderData, baseURL)
    
    return headers

def sendLendOrder(order):

    baseURL, headers, orderData = order
    response = requests.post(baseURL, headers=headers, data=json.dumps(orderData))
    pushToChannels(response, orderData)

def pushToChannels(response, orderData):

    currencyTicker = orderData['currency']
    amountLent = orderData['size']
    dailyIntRate = orderData['dailyIntRate']

    message = buildMessage(response, currencyTicker, amountLent, dailyIntRate)

    messageDiscord.push(message)

def buildMessage(response, currencyTicker, amountLent, dailyIntRate):
    if json.loads(response.text)['code'] != "200000":
        return f"Lend order failed with message: {response.text}"
    else:
        return f"Order {response.text} succesful! Lent {amountLent} USDT @ {dailyIntRate}%."

if __name__ == "__main__":
    autoLend("USDT")