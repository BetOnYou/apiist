from unittest import TestCase

import apiist


class TestTransactions(TestCase):
    def test_1_single_transaction(self):
        with apiist.transaction("single-transaction"):
            pass

    def test_2_two_transactions(self):
        with apiist.transaction("transaction-1"):
            pass
        with apiist.transaction("transaction-2"):
            pass

    def test_3_nested_transactions(self):
        with apiist.transaction("outer"):
            with apiist.transaction("inner"):
                pass

    def test_4_no_transactions(self):
        pass

    def test_5_apiist_assertions(self):
        apiist.http.get("http://blazedemo.com/").assert_ok()

    def test_6_apiist_assertions_failed(self):
        apiist.http.get(
            "http://blazedemo.com/"
        ).assert_failed()  # this assertion intentionally fails

    def test_7_failed_request(self):
        apiist.http.get("http://notexists")

    def test_8_assertion_trace_problem(self):
        resp = apiist.http.get("http://blazedemo.com/")
        resp.assert_regex_in_body(".*")
        resp.assert_regex_in_body(".+")
        resp.assert_regex_in_body("no way this exists in body")
