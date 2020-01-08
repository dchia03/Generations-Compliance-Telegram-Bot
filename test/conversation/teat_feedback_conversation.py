import unittest
from main.utils.logger import Logger


class TestFeedbackConversation(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
