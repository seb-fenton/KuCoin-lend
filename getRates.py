import requests 


def getDailyLendingRate(currency):
    """ Retrieve the most competitive current 7-day interest rate for
        the given currency ticker. 
    
    Keyword arguments:
    currency -- coin ticker (i.e. BTC, USDT) to find the rate for
    keyFile -- must be a json file containing passphrase, secret and key
    """
    baseURL = "https://api.kucoin.com"
    response = requests.get(baseURL + f"/api/v1/margin/market?currency={currency}&term=7")

    # returns lowest daily interest rate currently lent at for the currency
    return response.json()['data'][0]['dailyIntRate']


if __name__ == "__main__":
    getDailyLendingRate("USDT")