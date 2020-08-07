####################
## Module Imports ##
####################
from telegram import (
    ReplyKeyboardRemove
)
from telegram.ext import (
    CommandHandler, MessageHandler, Filters, ConversationHandler
)

###############
## Constants ##
###############
from main.constants.field import *
##############
## Document ##
##############
from main.database.member import Member
##############
## Database ##
##############
from main.stores.database_store import admin_db
######################
## Helper Functions ##
######################
from main.stores.helper_function_store import (
    init,
    typing_action,
    make_keyboard_reply_markup,
    refactor_keyboard_layout,
    make_reply_text,
    make_options_text_and_reply_markup,
)
##################
## ReplyOptions ##
##################
from main.stores.reply_option_store import (
    ADMIN, ADMIN_REPLY,
    ENTER_MEMBER_DATA, ENTER_DATA_FIELD, SUBMIT_MEMBER_DATA, SUBMIT_MEMBER_DATA_REPLY,
    UPDATE_MEMBER_DATA, UPDATE_MEMBER_DATA_REPLY, UPDATE_DATA_FIELD_VALUE, DELETE_MEMBER_DATA,
    DELETE_DATA_FROM_DATABASE,
    BACK, QUIT, CANCEL,
    UNKNOWN_REPLY_MSG
)
############
## Logger ##
############
from main.utils.logger import Logger

logger = Logger(__name__)


def basic_log(function_name, user_name, msg):
    logger.info("{}-> User {} replied: {}.".format(function_name, user_name, msg))


#########
# Admin #
#########
def admin_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("admin_start", user.first_name, msg)
    member_details_doc = admin_db.get_document(filter={FIELD_TELEGRAM_ID: str(user.id)})
    member_details = Member(member_details=member_details_doc)
    if member_details_doc is None:
        reply_options_list = [[ENTER_MEMBER_DATA], [QUIT]]
    else:
        reply_options_list = [[UPDATE_MEMBER_DATA, DELETE_MEMBER_DATA], [QUIT]]
    options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
    update.message.reply_text(
        text=make_reply_text([member_details.get_member_str(), options_text]),
        reply_markup=reply_markup
    )
    return ADMIN_REPLY.get_name()


def admin_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("admin_reply", user.first_name, msg)
    if ENTER_MEMBER_DATA.reply_check(msg):
        return enter_start(bot, update, user_data)
    elif UPDATE_MEMBER_DATA.reply_check(msg):
        return update_member_data_start(bot, update, user_data)
    elif DELETE_MEMBER_DATA.reply_check(msg):
        return delete_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return admin_start(bot, update, user_data)


##########
# Update #
##########
def update_member_data_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("update_start", user.first_name, msg)
    if "member_details_str" not in user_data.keys():
        user_data["member_details"] = Member(
            member_details=admin_db.get_document(
                filter={FIELD_TELEGRAM_ID: str(user.id)}
            )
        )
        user_data["member_details_str"] = user_data["member_details"].get_member_str()
    reply_options_list = refactor_keyboard_layout(Member.EDITABLE_FIELDS) \
                         + [[SUBMIT_MEMBER_DATA], [BACK, QUIT]]
    options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
    reply_text = make_reply_text(
        [
            user_data["member_details_str"],
            options_text,
            "Select Field to Update"
        ]
    )
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup
    )
    return UPDATE_MEMBER_DATA_REPLY.get_name()


def update_member_data_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("update_start_reply", user.first_name, msg)
    if SUBMIT_MEMBER_DATA.reply_check(msg):
        return update_submit(bot, update, user_data)
    elif BACK.reply_check(msg):
        return admin_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    elif msg in Member.EDITABLE_FIELDS:
        return update_data_field(bot, update, user_data)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return update_member_data_start(bot, update, user_data)


def update_data_field(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("update_data_field", user.first_name, msg)
    if "editing_field" not in user_data.keys() or user_data["editing_field"] is None:
        user_data["editing_field"] = msg
    update.message.reply_text(
        text=make_reply_text(
            [
                "Updating Records",
                "Enter {}: ".format(user_data["editing_field"]),
                "E.g. " + Member.ALL_FIELDS_ENTRY_EGS[user_data["editing_field"]]
            ]
        ),
        reply_markup=Member.ALL_FIELDS_REPLY_MARKUP[user_data["editing_field"]]
    )
    return UPDATE_DATA_FIELD_VALUE.get_name()


def update_data_field_value(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("update_data_reply", user.first_name, msg)
    if not user_data["member_details"].update_datafield(field=user_data["editing_field"], data=msg):
        update.message.reply_text(text="Invalid Input: {}".format(msg), reply_markup=ReplyKeyboardRemove())
        return update_data_field(bot, update, user_data)
    else:
        user_data["member_details_str"] = user_data["member_details"].get_member_str()
        user_data["editing_field"] = None
        return update_member_data_start(bot, update, user_data)


def update_submit(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("update_submit", user.first_name, msg)
    update.message.reply_text(text="Updating member details in database", reply_markup=ReplyKeyboardRemove())
    admin_db.update_document(user_data["member_details"])
    update.message.reply_text(text="Details Updated!\n" + "Going back Admin Menu", reply_markup=ReplyKeyboardRemove())
    return admin_start(bot, update, user_data)


#########
# Enter #
#########
def enter_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("enter_start", user.first_name, msg)
    user_data["member_details"] = Member(telegram_id=str(user.id))
    user_data["pos"] = 0
    enter_data_field_reply_format(bot, update, user_data)
    return ENTER_DATA_FIELD.get_name()


def enter_data_field_reply_format(bot, update, user_data):
    field = Member.EDITABLE_FIELDS[user_data["pos"]]
    update.message.reply_text(
        make_reply_text([
            "Field {} of {}\n".format(user_data["pos"] + 1, len(Member.EDITABLE_FIELDS)),
            "Enter {}:".format(field),
            "E.g. {}".format(Member.ALL_FIELDS_ENTRY_EGS[field])
        ]),
        reply_markup=Member.ALL_FIELDS_REPLY_MARKUP[field]
    )


def enter_data_field(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("enter_data_field", user.first_name, msg)
    if user_data["member_details"].set_datafield(field=Member.EDITABLE_FIELDS[user_data["pos"]], data=msg):
        user_data["pos"] += 1
        if user_data["pos"] < len(Member.EDITABLE_FIELDS):
            enter_data_field_reply_format(bot, update, user_data)
            return ENTER_DATA_FIELD.get_name()
        else:
            del user_data["pos"]
            return enter_data_submit(bot, update, user_data)
    else:
        update.message.reply_text("Invalid Entry: {}\nRe-enter value".format(msg))
        typing_action(bot, update)
        enter_data_field_reply_format(bot, update, user_data)
        return ENTER_DATA_FIELD.get_name()


def enter_data_submit(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("enter_data_submit", user.first_name, msg)
    unconfirmed_member_data_str = user_data["member_details"].get_member_str()
    options_text, reply_markup = make_options_text_and_reply_markup(
        [
            [SUBMIT_MEMBER_DATA],
            [BACK, QUIT]
        ]
    )
    update.message.reply_text(
        text=make_reply_text([unconfirmed_member_data_str, options_text]),
        reply_markup=reply_markup
    )
    return SUBMIT_MEMBER_DATA_REPLY.get_name()


def enter_data_submit_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("enter_data_submit_reply", user.first_name, msg)
    if SUBMIT_MEMBER_DATA.reply_check(msg):
        return enter_data_submit_to_database(bot, update, user_data)
    elif BACK.reply_check(msg):
        return enter_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(
            UNKNOWN_REPLY_MSG.get_description(),
            reply_markup=ReplyKeyboardRemove()
        )
        return enter_data_submit(bot, update, user_data)


def enter_data_submit_to_database(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("enter_data_submit_to_database", user.first_name, msg)
    update.message.reply_text("Uploading Data to Database")
    typing_action(bot, update)
    admin_db.add_document(user_data["member_details"])
    update.message.reply_text("Upload Completed\n" + "Returning to Main Menu")
    return admin_start(bot, update, user_data)


##########
# Delete #
##########
def delete_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("delete_start", user.first_name, msg)
    update.message.reply_text(
        "Are you sure you want to delete your data?",
        reply_markup=make_keyboard_reply_markup([["Yes", "No"]])
    )
    return DELETE_DATA_FROM_DATABASE.get_name()


def delete_data_from_database(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("delete_data_from_database", user.first_name, msg)
    if msg.lower() not in ["yes", "no"]:
        update.message.reply_text(
            "Invalid Reply",
            reply_markup=ReplyKeyboardRemove()
        )
        return delete_start(bot, update, user_data)
    elif msg.lower() == "yes":
        update.message.reply_text(
            "Removing Data",
            reply_markup=ReplyKeyboardRemove()
        )
        admin_db.delete_document(Member(admin_db.get_document(filter={FIELD_TELEGRAM_ID: str(user.id)})))
        typing_action(bot, update)
        update.message.reply_text(
            "Data Removed\n" + "Returning to Main Menu",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.message.reply_text(
            "Remove Cancelled\n" + "Returning to Main Menu",
            reply_markup=ReplyKeyboardRemove()
        )
    return admin_start(bot, update, user_data)


################################
## Fallback Callback Function ##
################################
def cancel(bot, update):
    user, msg = init(bot, update)
    basic_log("cancel", user.first_name, msg)
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text(
        "Session Ended",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


################################################
### Administration List Conversation Handler ###
################################################
admin_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(ADMIN.get_name(), admin_start, pass_user_data=True)
    ],
    states={
        ADMIN_REPLY.get_name(): [
            MessageHandler(Filters.text, admin_reply, pass_user_data=True)
        ],
        UPDATE_MEMBER_DATA_REPLY.get_name(): [
            MessageHandler(Filters.text, update_member_data_reply, pass_user_data=True)
        ],
        UPDATE_DATA_FIELD_VALUE.get_name(): [
            MessageHandler(Filters.text, update_data_field_value, pass_user_data=True)
        ],
        ENTER_DATA_FIELD.get_name(): [
            MessageHandler(Filters.text, enter_data_field, pass_user_data=True)
        ],
        SUBMIT_MEMBER_DATA_REPLY.get_name(): [
            MessageHandler(Filters.text, enter_data_submit_reply, pass_user_data=True)
        ],
        DELETE_DATA_FROM_DATABASE.get_name(): [
            MessageHandler(Filters.text, delete_data_from_database, pass_user_data=True)
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL.get_name(), cancel)
    ]
)
