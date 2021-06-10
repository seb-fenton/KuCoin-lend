import unittest
import os
import inspect 
import sys

sys.path.append('/Users/sf/Documents/Trading Projects/KuCoin Lend/')

from autoLend import buildOrderData

class TestAutoLend(unittest.TestCase):

    def test_orderBuilder(self):
        testOrder = buildOrderData('TEST', '0', '0')
        self.assertEqual(testOrder, 
                {'currency': 'TEST',
                 'dailyIntRate': '0', 
                 'size': '0', 
                 'term': 7
                })

if __name__ == '__main__':
    unittest.main()
