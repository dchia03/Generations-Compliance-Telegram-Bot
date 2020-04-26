import unittest
from unittest.mock import MagicMock

import bson

from main.conversation.administration_conversation import *
from main.utils.logger import Logger


class TestAdministrationConversation(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)

    def test_admin_start(self, find):
        bot = MagicMock()
        update = MagicMock(**{
            "message.from_user.first_name": "test_user",
            "message.text": "test_msg"
        })
        res = admin_start(bot, update, user_data={})
        assert(res == ADMIN_REPLY.get_name())

    def test_admin_reply(self):
        for expected, text_msg in zip(
            [
                ENTER_DATA_FIELD.get_name(), UPDATE_MEMBER_DATA_REPLY.get_name(),
                DELETE_DATA_FROM_DATABASE.get_name(), ConversationHandler.END,
                ADMIN_REPLY.get_name()
            ],
            [
                ENTER_MEMBER_DATA.get_name(), UPDATE_MEMBER_DATA.get_name(),
                DELETE_MEMBER_DATA.get_name(), QUIT.get_name(),
                "test_msg"
            ]
        ):
            self.log.info('Testing reply: ' + text_msg)
            bot = MagicMock()
            update = MagicMock(**{
                "message.from_user.first_name": "test_user",
                "message.from_user.id": "1234",
                "message.text": text_msg
            })
            user_data = {}
            actual = admin_reply(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)

    def test_update_member_data_reply(self):
        for expected, text_msg in zip(
            [
                ADMIN_REPLY.get_name(), ADMIN_REPLY.get_name(),
                ConversationHandler.END, UPDATE_MEMBER_DATA_REPLY.get_name(),
                UPDATE_DATA_FIELD_VALUE.get_name()
            ],
            [
                SUBMIT_MEMBER_DATA.get_name(), BACK.get_name(),
                QUIT.get_name(), "test_msg",
                'Name'
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
                'member_details': Member(
                    member_details={
                        '_id': bson.objectid.ObjectId('5e1044518fb4e47cd1e9804e'),
                        'Telegram ID': '1234', 'Name': 'test_user', 'Full Name': 'test_user', 'DOB': '01/01/2020',
                        'HP': '91234567', 'Cell Group': '1.1', 'Cell Leader': 'John Smith', 'Baptised': 'Yes',
                        'Role': 'Member', 'Date Updated': '01/01/2020 00:00:00', 'Date Created': '01/01/2020 00:00:00'
                    }
                )
            }

            actual = update_member_data_reply(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)

    def test_update_data_field_value(self):
        for expected, text_msg in zip(
            [
                UPDATE_MEMBER_DATA_REPLY.get_name(), UPDATE_DATA_FIELD_VALUE.get_name()
            ],
            [
                "test user updated", "test_user_updated"
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
                'member_details': Member(
                    member_details={
                        '_id': bson.objectid.ObjectId('5e1044518fb4e47cd1e9804e'),
                        'Telegram ID': '1234', 'Name': 'test_user', 'Full Name': 'test_user', 'DOB': '01/01/2020',
                        'HP': '91234567', 'Cell Group': '1.1', 'Cell Leader': 'John Smith', 'Baptised': 'Yes',
                        'Role': 'Member', 'Date Updated': '01/01/2020 00:00:00', 'Date Created': '01/01/2020 00:00:00'
                    }
                ),
                'editing_field': 'Name'
            }

            actual = update_data_field_value(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)

    def test_enter_data_field(self):
        for expected, text_msg, pos in zip(
            [
                ENTER_DATA_FIELD.get_name(), SUBMIT_MEMBER_DATA_REPLY.get_name(), ENTER_DATA_FIELD.get_name()
            ],
            [
                "new test user name", "Yes", "invalid_name"
            ],
            [
                1, len(Member.EDITABLE_FIELDS) - 1, 1
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

            actual = enter_data_field(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)

    def test_enter_data_submit(self):
        expected = SUBMIT_MEMBER_DATA_REPLY.get_name()
        bot = MagicMock()
        update = MagicMock(**{
            "message.from_user.first_name": "test_user",
            "message.from_user.id": "1234",
            "message.text": None
        })
        user_data = {
            "member_details": Member(telegram_id="1234")
        }

        actual = enter_data_submit(bot, update, user_data)
        self.log.info("User Data: " + str(user_data))
        assert (actual == expected)

    def test_enter_data_submit_reply(self):
        for expected, text_msg in zip(
            [
                ADMIN_REPLY.get_name(), ENTER_DATA_FIELD.get_name(), ConversationHandler.END, SUBMIT_MEMBER_DATA_REPLY.get_name()
            ],
            [
                SUBMIT_MEMBER_DATA.get_name(), BACK.get_name(), QUIT.get_name(), "INVALID_REQUEST"
            ]
        ):
            self.log.info('Testing reply: ' + text_msg)
            bot = MagicMock()
            update = MagicMock(**{
                "message.from_user.first_name": "test_user",
                "message.from_user.id": "4321",
                "message.text": text_msg
            })
            user_data = {"member_details": Member(telegram_id="4321")}
            actual = enter_data_submit_reply(bot, update, user_data)
            self.log.info("User Data: " + str(user_data))
            assert (actual == expected)

        self.log.info("Test Delete")
        expected = ADMIN_REPLY.get_name()
        bot = MagicMock()
        update = MagicMock(**{
            "message.from_user.first_name": "test_user",
            "message.from_user.id": "4321",
            "message.text": "Yes"
        })
        user_data = {}
        actual = delete_data_from_database(bot, update, user_data)
        self.log.info("User Data: " + str(user_data))
        assert (actual == expected)
