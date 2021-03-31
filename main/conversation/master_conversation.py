####################
## Module Imports ##
####################
from telegram import (
    ReplyKeyboardRemove
)
from telegram.ext import (
    CommandHandler, MessageHandler, Filters, ConversationHandler
)

##############
## Database ##
##############
from main.__main__ import cancel
from main.entity.collection.impl.admin_collection import admin_collection
######################
## Helper Functions ##
######################
from main.stores.helper_function_store import (
    init,
    make_reply_text,
    make_options_text_and_reply_markup,
)
############
## Logger ##
############
from main.stores.reply_option_store import MASTER, MASTER_REPLY, CANCEL, UNAUTHORISED_ACCESS_MSG, QUIT, \
    MASTER_MEMBER_DETAILS, MASTER_ROSTER, UNKNOWN_REPLY_MSG, BACK, MASTER_DELETE, \
    MASTER_EDIT, MASTER_MEMBER_DETAILS_REPLY, MASTER_VIEW_MEMBER_DETAILS_REPLY, MASTER_SUBMIT, \
    MASTER_EDIT_MEMBER_DETAILS_REPLY
from main.utils.logger import Logger

##############
## Document ##
##############

logger = Logger(__name__)


def basic_log(function_name, user_name, msg):
    logger.info("{}-> User {} replied: {}.".format(function_name, user_name, msg))


##########
# Master #
##########
def master_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_start", user.first_name, msg)
    member_details = admin_collection.get_member(str(user.id))
    if not member_details.is_ministry_head():
        update.message.reply_text(
            text=UNAUTHORISED_ACCESS_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        reply_options_list = [[MASTER_MEMBER_DETAILS, MASTER_ROSTER], [QUIT]]
        options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
        update.message.reply_text(
            text=make_reply_text([options_text]),
            reply_markup=reply_markup
        )
        return MASTER_REPLY.get_name()


def master_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_reply", user.first_name, msg)
    if MASTER_MEMBER_DETAILS.reply_check(msg):
        return master_member_details(bot, update, user_data)
    elif MASTER_ROSTER.reply_check(msg):
        update.message.reply_text(
            "Not Implemented",
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)


def master_member_details(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_member_details", user.first_name, msg)
    member_details = admin_collection.get_member(str(user.id))
    if not member_details.is_ministry_head():
        update.message.reply_text(
            text=UNAUTHORISED_ACCESS_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        reply_options_list = [admin_collection.get_all_members_name(), [BACK, QUIT]]
        options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
        update.message.reply_text(
            text=make_reply_text(["Select Member", options_text]),
            reply_markup=reply_markup
        )
        return MASTER_MEMBER_DETAILS_REPLY.get_name()


def master_member_details_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_member_details_reply", user.first_name, msg)
    if BACK.reply_check(msg):
        return master_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    elif msg in admin_collection.get_all_members_name():
        return master_view_member_details(bot, update, user_data)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)


def master_view_member_details(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_member_details", user.first_name, msg)
    member_details = admin_collection.get_member(str(user.id))
    user_data['view_member_name'] = msg
    if not member_details.is_ministry_head():
        update.message.reply_text(
            text=UNAUTHORISED_ACCESS_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        user_data["viewing_member"] = admin_collection.get_member_from_name(user_data['view_member_name'])
        reply_options_list = [[MASTER_EDIT, MASTER_DELETE], [BACK, QUIT]]
        options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
        update.message.reply_text(
            text=make_reply_text([user_data["viewing_member"].get_member_str(), options_text]),
            reply_markup=reply_markup
        )
        return MASTER_VIEW_MEMBER_DETAILS_REPLY.get_name()


def master_view_member_details_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_member_details_reply", user.first_name, msg)
    if BACK.reply_check(msg):
        return master_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    elif MASTER_EDIT.reply_check(msg):
        return master_edit_member_details(bot, update, user_data)
    elif MASTER_DELETE.reply_check(msg):
        update.message.reply_text(
            "Not Implemented",
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)


def master_edit_member_details(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_edit_member_details", user.first_name, msg)
    member_details = admin_collection.get_member(str(user.id))
    if not member_details.is_ministry_head():
        update.message.reply_text(
            text=UNAUTHORISED_ACCESS_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        reply_options_list = [
            [user_data["viewing_member"].get_master_editable_fields()],
            [MASTER_SUBMIT], [BACK, QUIT]
        ]
        options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
        update.message.reply_text(
            text=make_reply_text([
                user_data["viewing_member"].get_member_str(),
                "Select Detail Field to Edit",
                options_text
            ]),
            reply_markup=reply_markup
        )
        return MASTER_EDIT_MEMBER_DETAILS_REPLY.get_name()


def master_edit_member_details_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("master_edit_member_details_reply", user.first_name, msg)
    if BACK.reply_check(msg):
        return master_view_member_details(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    elif MASTER_SUBMIT.reply_check(msg):
        update.message.reply_text(
            "Not Implemented",
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)
    elif msg in user_data["viewing_member"].get_master_editable_fields():

        return master_edit_member_details(bot, update, user_data)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return master_start(bot, update, user_data)


###########################################
### Master Control Conversation Handler ###
###########################################
admin_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(MASTER.get_name(), master_start, pass_user_data=True)
    ],
    states={
        MASTER_REPLY.get_name(): [
            MessageHandler(Filters.text, master_reply, pass_user_data=True)
        ],
        MASTER_MEMBER_DETAILS_REPLY: [
            MessageHandler(Filters.text, master_member_details_reply, pass_user_data=True)
        ],
        MASTER_VIEW_MEMBER_DETAILS_REPLY: [
            MessageHandler(Filters.text, master_view_member_details_reply, pass_user_data=True)
        ],
        MASTER_EDIT_MEMBER_DETAILS_REPLY: [
            MessageHandler(Filters.text, master_edit_member_details_reply, pass_user_data=True)
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL.get_name(), cancel)
    ]
)
