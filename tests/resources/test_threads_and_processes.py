import os
import unittest


import apiritif
from apiritif import thread_indexes
from apiritif.feeders import CSVFeeder

feeder = CSVFeeder(os.path.join(os.path.dirname(__file__), "data/source.csv"))


def log_it(name, data):
    log_line = "%s-%s. %s:%s\n" % (thread_indexes()[1], name, data["name"], data["pass"])
    with apiritif.transaction(log_line):
        pass


def setup():    # setup_module
    feeder.read_vars()  # todo: close reader in nose_run


class Test0(unittest.TestCase):
    def test_00(self):
        log_it("00", feeder.get_vars())


class Test1(unittest.TestCase):
    def setUp(self):
        self.vars = feeder.get_vars()

    def test_10(self):
        log_it("10", self.vars)

    def test_11(self):
        log_it("11", self.vars)
