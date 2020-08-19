import unittest
from main.utils.logger import Logger
from main.utils.reply_option import ReplyOption


class TestReplyOption(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.base_log_msg = 'Testing {}: '.format(__name__)

    def test_reply_option_functions(self):
        reply_option_1 = ReplyOption("ro1")
        reply_option_2 = ReplyOption("ro2", "reply option 2")
        assert(repr(reply_option_1) == "ro1")
        assert(str(reply_option_1) == "ro1")
        assert(reply_option_1.get_description() == "")
        assert(reply_option_2.get_description() == "ro2: reply option 2")
        assert(reply_option_1.get_name() == "ro1")
        assert(reply_option_1.reply_check("ro1"))
