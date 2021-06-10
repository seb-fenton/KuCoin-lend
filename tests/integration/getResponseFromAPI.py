import unittest
import os
import inspect 
import sys
import dotenv

sys.path.append('/Users/sf/Documents/Trading Projects/KuCoin Lend/')
import autoLend

# Once my kucoin test subaccount gets approved,
# I'll be using this to run integration testing

if __name__ == "__main__":
    dotenv_path = Path('.testenv')
    load_dotenv(dotenv_path=dotenv_path)