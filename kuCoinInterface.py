import json
import requests

from utility.readVars import readKeysFromEnv
from utility.buildHeaders import generateHeadersJson

def getAvailable(currencyTicker):

    baseURL = "https://api.kucoin.com/api/v1/accounts"

    apiKey, apiSecret, apiPassphrase = readKeysFromEnv()
    headers = generateHeadersJson(apiKey, apiSecret, apiPassphrase, "", baseURL)

    response = requests.get(baseURL, headers=headers)
    available = scrapeResponse(response, currencyTicker)

    return available

def scrapeResponse(response, targetCurrency):

    for currencyBlock in response.json()['data']:
        if currencyBlock['currency'] == targetCurrency and currencyBlock['type'] == 'main':
            available = currencyBlock['available']
            return available

    raise BaseException('Currency not found in account')

def getDailyLendingRate(currencyTicker):
    """ Retrieve the most competitive current 7-day interest rate for
        the given currency ticker. 
    """
    baseURL = "https://api.kucoin.com"

    response = requests.get(baseURL + f"/api/v1/margin/market?currency={currencyTicker}&term=7")
    lowestDailyInterestRate = response.json()['data'][0]['dailyIntRate']
    
    return lowestDailyInterestRate 


if __name__ == "__main__":
    getDailyLendingRate("USDT")