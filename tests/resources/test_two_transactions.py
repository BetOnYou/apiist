import logging
import random
import string
import sys
import time
import unittest

import apiist


class TestTwoTransactions(unittest.TestCase):

    def first(self):
        with apiist.smart_transaction('1st'):
            response = apiist.http.get('https://blazedemo.com/')
            response.assert_ok()

    def second(self):
        with apiist.smart_transaction('2nd'):
            response = apiist.http.get('https://blazedemo.com/vacation.html')

    def test_simple(self):
        self.first()
        self.second()
