import unittest
import os
import inspect 
import sys

sys.path.append('/Users/sf/Documents/Trading Projects/KuCoin Lend/')

from kuCoinInterface import getDailyLendingRate

class TestAutoLend(unittest.TestCase):

    def test_dailyLendingRate(self):
        correctRate = float(getDailyLendingRate("USDT"))
        self.assertEqual(isinstance(correctRate, float), True)

if __name__ == '__main__':
    unittest.main()
