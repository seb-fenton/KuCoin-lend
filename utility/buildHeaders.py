import json
import time
import hashlib
import hmac
import base64

def generateHeadersJson(apiKey, apiSecret, apiPassphrase, orderData, baseURL):
    now = int(time.time() * 1000)
    apiURL = baseURL.replace("https://api.kucoin.com","")
    HTTPType, orderDataJson = handleOrderData(orderData)
    stringToSign = str(now) + HTTPType + apiURL + orderDataJson

    signature = base64.b64encode(hmac.new(apiSecret.encode('utf-8'), stringToSign.encode('utf-8'), hashlib.sha256).digest())
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


def handleOrderData(orderData):

    orderDataJson = json.dumps(orderData) if orderData != "" else ""

    HTTPType = 'POST'
    if orderDataJson == "":
        HTTPType = 'GET'
    
    return HTTPType, orderDataJson