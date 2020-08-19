############################
## Conversation Functions ##
############################

import datetime as dt

import telegram
from telegram import (
    KeyboardButton, ReplyKeyboardMarkup
)

from main.utils.reply_option import ReplyOption


#######################
# Common Conversation #
#######################
def init(bot, update):
    typing_action(bot, update)
    user = update.message.from_user
    msg = update.message.text
    return user, msg


def basic_log(logger, function_name, user_name, msg):
    logger.info("{}-> User {} replied: {}.".format(function_name, user_name, msg))


def typing_action(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)


def make_keyboard_reply_markup(keyboard):
    kb = []
    for row in keyboard:
        kb_row = []
        for callback_data in row:
            kb_row.append(KeyboardButton(callback_data, callback_data=callback_data))
        kb.append(kb_row)
    reply_markup = ReplyKeyboardMarkup(
        kb,
        one_time_keyboard=True,
        resize_keyboard=True,
        selective=True
    )
    return reply_markup


def refactor_keyboard_layout(kb, num_cols=2):
    new_kb = []
    while len(kb) > num_cols:
        new_kb.append(kb[:num_cols])
        kb = kb[num_cols:]
    if len(kb) > 0:
        new_kb.append(kb)
    return new_kb


def make_reply_text(text_list):
    msg = ""
    for text in text_list:
        msg += text + "\n"
    return msg


def make_options_text(options_list):
    msg = "Select Option:\n"
    return msg + make_reply_text(options_list)


def make_options_text_and_reply_markup(reply_options_list):
    kb = []
    for row in reply_options_list:
        kb_row = []
        for reply_option in row:
            label = ""
            if isinstance(reply_option, ReplyOption):
                label = reply_option.get_name()
            elif type(reply_option) == str:
                label = reply_option
            kb_row.append(KeyboardButton(label, callback_data=label))
        kb.append(kb_row)
    reply_markup = ReplyKeyboardMarkup(
        kb,
        one_time_keyboard=True,
        resize_keyboard=True,
        selective=True
    )
    options_text = make_options_text(
        [option.get_description() for row in reply_options_list for option in row if
         isinstance(option, ReplyOption) and option.get_description() is not None]
    )
    return options_text, reply_markup


######################
# Serve Conversation #
######################

def get_all_weekdays_in_month(wday, month, year):
    date_list = []
    curr_date = dt.date(year, month, 1)
    delta_days = (wday - curr_date.weekday()) % 7
    curr_date += dt.timedelta(days=delta_days)
    while curr_date.month == month:
        date_list.append(curr_date.day)
        curr_date += dt.timedelta(days=7)
    return date_list


def is_valid_bod_input_dates(msg, block_out_dates):
    msg = msg.strip()
    if msg == "0":
        return True
    msg_list = [m.strip() for m in msg.split(" ")]
    for d in msg_list:
        if d.isdigit():
            if d not in block_out_dates.get_datafield(field="Block Out Dates").keys():
                return False
        else:
            return False
    return True


def processed_member_input_block_out_dates(msg, block_out_dates):
    msg = msg.strip()
    if is_valid_bod_input_dates(msg, block_out_dates):
        if msg == "0":
            return []
        else:
            return [m.strip() for m in msg.split(" ")]
    else:
        return None
