import unittest
from unittest.mock import MagicMock

from main.conversation.feedback_conversation import *


class TestFeedbackConversation(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)

    def test_feedback_check_reply(self):
        for expected, text_msg in zip(
                [
                    ConversationHandler.END, FEEDBACK_CHECK.get_name(), ConversationHandler.END, FEEDBACK_CHECK.get_name()
                ],
                [
                    SEND.get_name(), BACK.get_name(), QUIT.get_name(), "INVALID"
                ]
        ):
            self.log.info('Testing reply: ' + text_msg)
            bot = MagicMock()
            update = MagicMock(**{
                "message.from_user.first_name": "test_user",
                "message.from_user.id": "1234",
                "message.text": text_msg
            })
            user_data = {
                "member_details": Member(telegram_id="1234"),
                'pos': pos
            }

            actual = feedback_check_reply(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)
