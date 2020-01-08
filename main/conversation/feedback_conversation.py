####################
## Module Imports ##
####################
import datetime as dt

from pytz import timezone
from telegram import (
    ReplyKeyboardRemove
)
from telegram.ext import (
    CommandHandler, MessageHandler, Filters, ConversationHandler
)

############
# Document #
############
from main.database.member import Member
###############
## Databases ##
###############
from main.stores.database_store import admin_db
from main.stores.helper_function_store import (
    init,
    make_reply_text,
    make_options_text_and_reply_markup
)
#############
## Strings ##
#############
from main.stores.reply_option_store import (
    FEEDBACK, FEEDBACK_CHECK, FEEDBACK_CHECK_REPLY,
    SEND,
    BACK, QUIT, CANCEL,
    UNKNOWN_REPLY_MSG
)
#############
## Logging ##
#############
from main.utils.logger import Logger

logger = Logger(__name__)


def basic_log(function_name, user_name, msg):
    logger.info("{}-> User {} replied: {}.".format(function_name, user_name, msg))


TIMEZONE = "Singapore"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


############
# Feedback #
############
def feedback_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("feedback_start", user.first_name, msg)
    update.message.reply_text(
        text=make_reply_text(
            [
                "Giving Feedback\n",
                "Type in any questions/queries you have regarding the Telegram Bot and it will be sent to the administrator.",
            ]
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    return FEEDBACK_CHECK.get_name()


def feedback_check(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("feedback_check", user.first_name, msg)
    user_data["msg"] = msg
    reply_options_list = [[SEND], [BACK, QUIT]]
    options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
    update.message.reply_text(
        text=make_reply_text(
            [
                "Your response:\n",
                msg + "\n",
                options_text
            ]
        ),
        reply_markup=reply_markup
    )
    return FEEDBACK_CHECK_REPLY.get_name()


def feedback_check_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("feedback_check_reply", user.first_name, msg)
    if SEND.reply_check(msg):
        return feedback_send(bot, update, user_data)
    elif BACK.reply_check(msg):
        return feedback_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return feedback_start(bot, update, user_data)


def feedback_send(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("feedback_check_reply", user.first_name, msg)
    administrator_details = Member(member_details=admin_db.get_document(filter={"Role": "Ministry Head"}))
    sender_details = Member(member_details=admin_db.get_document(filter={"Telegram ID": str(user.id)}))
    bot.send_message(
        chat_id=int(administrator_details.get_datafield("Telegram ID")),
        text=make_reply_text(
            [
                "From: {}".format(sender_details.get_datafield("Name")),
                "Created Date: {}".format(dt.datetime.now(timezone(TIMEZONE)).strftime(DATETIME_FORMAT)),
                "Query:",
                user_data["msg"]
            ]
        )
    )
    update.message.reply_text("Query Sent.\nEnding Session.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


################################
## Fallback Callback Function ##
################################
def cancel(bot, update):
    user, msg = init(bot, update)
    basic_log("cancel", user.first_name, msg)
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text(
        text="Session Ended",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


#####################################
### Feedback Conversation Handler ###
#####################################
feedback_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(FEEDBACK.get_name(), feedback_start, pass_user_data=True)
    ],
    states={
        FEEDBACK_CHECK.get_name(): [
            MessageHandler(Filters.text, feedback_check, pass_user_data=True)
        ],
        FEEDBACK_CHECK_REPLY.get_name(): [
            MessageHandler(Filters.text, feedback_check_reply, pass_user_data=True)
        ],
    },
    fallbacks=[
        CommandHandler(CANCEL.get_name(), cancel)
    ]
)
