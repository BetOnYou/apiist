import math
from unittest import TestCase

import apiist


def setUpModule():
    raise BaseException


class TestSimple(TestCase):
    def test_case1(self):
        # apiist.http.get("http://localhost:8003")
        with apiist.transaction("tran name"):
            for x in range(1000, 10000):
                y = math.sqrt(x)
