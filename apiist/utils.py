"""
Copyright 2017 BlazeMeter Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import os
import re
import sys
import traceback

VERSION = "1.0.0"

log = logging.getLogger("apiist")


def get_trace(error):
    if sys.version > "3":
        # noinspection PyArgumentList
        exct, excv, trace = error
        if isinstance(excv, str):
            excv = exct(excv)
        lines = traceback.format_exception(exct, excv, trace, chain=True)
    else:
        lines = traceback.format_exception(*error)
    return "".join(lines).rstrip()


def graceful():
    graceful_file_name = os.environ.get("GRACEFUL")
    graceful_flag = graceful_file_name and os.path.exists(graceful_file_name)
    return graceful_flag


class NormalShutdown(BaseException):
    pass


def headers_as_text(headers_dict):
    return "\n".join("%s: %s" % (key, value) for key, value in headers_dict.items())


def shorten(string, upto, end_with="..."):
    return string[: upto - len(end_with)] + end_with if len(string) > upto else string


def assert_regexp(regex, text, match=False, msg=None):
    if match:
        if re.match(regex, text) is None:
            msg = msg or "Regex %r didn't match expected value: %r" % (regex, shorten(text, 100))
            raise AssertionError(msg)
    else:
        if not re.findall(regex, text):
            msg = msg or "Regex %r didn't find anything in text %r" % (regex, shorten(text, 100))
            raise AssertionError(msg)


def assert_not_regexp(regex, text, match=False, msg=None):
    if match:
        if re.match(regex, text) is not None:
            msg = msg or "Regex %r unexpectedly matched expected value: %r" % (
                regex,
                shorten(text, 100),
            )
            raise AssertionError(msg)
    else:
        if re.findall(regex, text):
            msg = msg or "Regex %r unexpectedly found something in text %r" % (
                regex,
                shorten(text, 100),
            )
            raise AssertionError(msg)
