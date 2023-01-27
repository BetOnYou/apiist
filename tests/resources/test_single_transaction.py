import logging
import random
import string
import sys
import time
import unittest

import apiist


class TestAPIRequests(unittest.TestCase):

    def test_requests(self):
        with apiist.transaction('blazedemo 123'):
            response = apiist.http.get('https://api.demoblaze.com/entries', allow_redirects=True)
            response.assert_jsonpath('$.LastEvaluatedKey.id', expected_value='9')
        time.sleep(0.75)

        with apiist.transaction('blazedemo 456'):
            response = apiist.http.get('https://api.demoblaze.com/entries', allow_redirects=True)
            response.assert_jsonpath("$['LastEvaluatedKey']['id']", expected_value='9')
        time.sleep(0.75)
