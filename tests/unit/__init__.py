import os

from urllib3 import disable_warnings

from apiist.loadgen import ApiritifPlugin

disable_warnings()

RESOURCES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/../resources/")
)


class Recorder(ApiritifPlugin):
    configSection = "recorder-plugin"
    alwaysOn = True

    def __init__(self):
        super().__init__()
        self.session.stop_reason = ""
