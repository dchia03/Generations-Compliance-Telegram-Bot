####################
## Module Imports ##
####################
import datetime as dt

from telegram import (
    ReplyKeyboardRemove
)
from telegram.ext import (
    CommandHandler, MessageHandler, Filters, ConversationHandler
)

from main.entity.collection.impl.admin_collection import admin_collection
from main.entity.collection.impl.block_out_dates_collection import block_out_dates_collection
###############
## Databases ##
###############
from main.entity.collection.impl.roster_collection import roster_collection
###############
## Documents ##
###############
from main.entity.document.impl.block_out_dates import BlockOutDates
from main.entity.document.impl.member import Member
######################
## Helper Functions ##
######################
from main.stores.helper_function_store import (
    init,
    typing_action,
    make_reply_text,
    make_options_text_and_reply_markup,
    get_all_weekdays_in_month,
    is_valid_bod_input_dates,
    processed_member_input_block_out_dates
)
#############
## Strings ##
#############
from main.stores.reply_option_store import (
    SERVE, SERVE_REPLY,
    ROSTER, ROSTER_REPLY,
    REMIND,
    CREATE, CREATE_REPLY, CHECK_ROSTER_REPLY, RECREATE_ROSTER, UPLOAD_ROSTER,
    SWAP, REPLACE, BLOCK_OUT_DATES, BLOCK_OUT_DATES_REPLY, BLOCK_OUT_DATES_SUBMIT, BLOCK_DATES,
    ENTER_BLOCK_OUT_DATES_MSG,
    UNAUTHORISED_USE_MSG,
    ERROR_MSG,
    UNAUTHORISED_ACCESS_MSG,
    BACK, QUIT, CANCEL,
    UNKNOWN_REPLY_MSG
)
from main.utils.logger import Logger
from main.utils.roster_maker_2 import build_roster

logger = Logger(__name__)


def basic_log(function_name, user_name, msg):
    logger.info("{}-> User {} replied: {}.".format(function_name, user_name, msg))


##########
# Serve ##
##########
def serve_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("serve_start", user.first_name, msg)
    if not admin_collection.has_member(str(user.id)):
        update.message.reply_text(
            text=UNAUTHORISED_ACCESS_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        latest_roster = roster_collection.get_latest_roster()
        member_details = admin_collection.get_member(str(user.id))
        member_roster_str = latest_roster.get_member_roster_dates_str(member_name=member_details.get_name())
        latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
        member_block_out_dates_str = latest_block_out_dates.get_member_block_out_dates_str(
            member_name=member_details.get_name()
        )
        reply_options_list = [[ROSTER, BLOCK_OUT_DATES], [SWAP, REPLACE], [QUIT]]
        options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
        update.message.reply_text(
            text=make_reply_text(
                [
                    member_roster_str,
                    member_block_out_dates_str,
                    options_text
                ]
            ),
            reply_markup=reply_markup
        )
        return SERVE_REPLY.get_name()


def serve_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("serve_reply", user.first_name, msg)
    if ROSTER.reply_check(msg):
        return roster_start(bot, update, user_data)
    elif BLOCK_OUT_DATES.reply_check(msg):
        return bod_start(bot, update, user_data)
    elif SWAP.reply_check(msg):
        return swap_dev(bot, update, user_data)
    elif REPLACE.reply_check(msg):
        return replace_dev(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return serve_start(bot, update, user_data)


##########
# Roster #
##########
def roster_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("roster_start", user.first_name, msg)
    reply_options_list = [[BACK, QUIT]]
    if admin_collection.is_ministry_head_role(str(user.id)):
        reply_options_list = [[CREATE], [BACK, QUIT]]
    latest_roster = roster_collection.get_latest_roster()
    member_details = admin_collection.get_member(str(user.id))
    member_roster_str = latest_roster.get_member_roster_dates_str(
        member_name=member_details.get_name()
    )
    options_text, reply_markup = make_options_text_and_reply_markup(reply_options_list)
    update.message.reply_text(
        text=make_reply_text(
            [
                latest_roster.get_roster_str(),
                member_roster_str,
                options_text
            ]
        ),
        reply_markup=reply_markup
    )
    return ROSTER_REPLY.get_name()


def roster_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("roster_reply", user.first_name, msg)
    if CREATE.reply_check(msg):
        if not admin_collection.is_ministry_head_role(str(user.id)):
            update.message.reply_text(UNAUTHORISED_USE_MSG, reply_markup=ReplyKeyboardRemove())
            return roster_start(bot, update, user_data)
        return create_start(bot, update, user_data)
    elif BACK.reply_check(msg):
        return serve_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return roster_start(bot, update, user_data)


##########
# Create #
##########
def create_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("create_start", user.first_name, msg)
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    options_text, reply_markup = make_options_text_and_reply_markup(
        reply_options_list=[[CREATE, REMIND], [BACK, QUIT]]
    )
    update.message.reply_text(
        text=make_reply_text([latest_block_out_dates.get_block_out_dates_str(), options_text]),
        reply_markup=reply_markup
    )
    return CREATE_REPLY.get_name()


def create_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("create_reply", user.first_name, msg)
    if CREATE.reply_check(msg):
        if not admin_collection.is_ministry_head_role(str(user.id)):
            update.message.reply_text(UNAUTHORISED_USE_MSG, reply_markup=ReplyKeyboardRemove())
            return roster_start(bot, update, user_data)
        return create_roster(bot, update, user_data)
    elif REMIND.reply_check(msg):
        return remind_members(bot, update, user_data)
    elif BACK.reply_check(msg):
        return roster_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return roster_start(bot, update, user_data)


def create_roster(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("create_roster", user.first_name, msg)
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    latest_roster = roster_collection.get_latest_roster()
    update.message.reply_text(
        text='Creating Roster for {} {}'.format(
            latest_block_out_dates.get_month(),
            latest_block_out_dates.get_year()
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    user_data["new_roster"] = build_roster(
        all_members=admin_collection.get_all_members(),
        block_out_dates_doc=latest_block_out_dates,
        prev_roster_doc=latest_roster
    )
    # user_data["new_roster"] = roster_maker(
    #     block_out_dates=latest_block_out_dates,
    #     all_members=admin_collection.get_all_members(),
    #     prev_roster=latest_roster
    # )
    return check_roster(bot, update, user_data)


def check_roster(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("check_roster", user.first_name, msg)
    options_text, reply_markup = make_options_text_and_reply_markup(
        reply_options_list=[[RECREATE_ROSTER, UPLOAD_ROSTER], [BACK, QUIT]]
    )
    update.message.reply_text(
        text=make_reply_text(
            [
                "Newly Created Roster",
                user_data["new_roster"].get_roster_str(),
                options_text
            ]
        ),
        reply_markup=reply_markup
    )
    return CHECK_ROSTER_REPLY.get_name()


def check_roster_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("check_roster_reply", user.first_name, msg)
    if RECREATE_ROSTER.reply_check(msg):
        return create_roster(bot, update, user_data)
    elif UPLOAD_ROSTER.reply_check(msg):
        return upload_roster(bot, update, user_data)
    elif BACK.reply_check(msg):
        return create_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return check_roster(bot, update, user_data)


def upload_roster(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("upload_roster", user.first_name, msg)
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    latest_roster = roster_collection.get_latest_roster()
    update.message.reply_text(
        text='Uploading Roster to Database',
        reply_markup=ReplyKeyboardRemove()
    )
    typing_action(bot, update)

    latest_block_out_dates_month = str(latest_block_out_dates.get_month())
    latest_block_out_dates_year = int(latest_block_out_dates.get_year())
    latest_block_out_dates_month_int = dt.datetime.strptime(latest_block_out_dates_month, '%B').month

    latest_roster_year = int(latest_roster.get_year())
    latest_roster_month_int = int(dt.datetime.strptime(latest_roster.get_month(), '%B').month)

    if not (
            latest_roster_month_int + 1 == latest_block_out_dates_month_int
            and latest_roster_year
            and latest_block_out_dates_year
    ) \
            and not (
            latest_roster_month_int + 1 == 13
            and latest_block_out_dates_month_int == 1
            and latest_roster_year + 1 == latest_block_out_dates_year
    ):
        update.message.reply_text(ERROR_MSG, reply_markup=ReplyKeyboardRemove())
        return create_start(bot, update, user_data)

    if latest_block_out_dates_month_int < 12:
        new_month_int = latest_block_out_dates_month_int + 1
        new_year = int(latest_block_out_dates_year)
    else:
        new_month_int = 1
        new_year = int(latest_block_out_dates_year) + 1

    new_block_out_dates = BlockOutDates(
        month=dt.datetime(year=new_year, month=new_month_int, day=1).strftime('%B'),
        year=int(new_year),
        block_out_dates={str(d): [] for d in get_all_weekdays_in_month(wday=5, month=new_month_int, year=new_year)},
        unconfirmed=[m.get_name() for m in admin_collection.get_all_members()]
    )

    roster_collection.add_roster(roster=user_data["new_roster"])
    block_out_dates_collection.add_block_out_dates(bod=new_block_out_dates)

    update.message.reply_text(
        'Upload Complete\n' +
        'Going back to Main Menu',
        reply_markup=ReplyKeyboardRemove()
    )
    return serve_start(bot, update, user_data)


def remind_members(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("remind_members", user.first_name, msg)
    update.message.reply_text("Sending Reminders to Members")
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    for name in latest_block_out_dates.get_unconfirmed():
        member_data = Member(member_details=admin_collection.get_document(filter={"Name": str(name)}))
        if member_data is not None:
            telegram_id = member_data.get_telegram_id()
            logger.info('Sending reminder to {}'.format(name))
            bot.send_message(
                chat_id=int(telegram_id),
                text="Hi {}\nPlease remember to update your serving availability for {} {}\n".format(
                    name, latest_block_out_dates.get_month(), latest_block_out_dates.get_year()
                ) + "Thank You and have a blessed day!"
            )
        else:
            logger.info('Unable to find member data for {}'.format(name))
    typing_action(bot, update)
    update.message.reply_text(
        "Members Reminded\n" +
        "Returning to Main Menu",
        reply_markup=ReplyKeyboardRemove()
    )
    return create_start(bot, update, user_data)


###########
# Replace #
###########
def replace_dev(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("replace_start", user.first_name, msg)
    update.message.reply_text(
        make_reply_text(
            [
                "Replace Duty Feature is still under development" + "\n",
                "Returning back to previous menu"
            ]
        )
    )
    return serve_start(bot, update, user_data)


########
# Swap #
########
def swap_dev(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("replace_start", user.first_name, msg)
    update.message.reply_text(
        make_reply_text(
            [
                "Swap Duty Feature is still under development" + "\n",
                "Returning back to previous menu"
            ]
        )
    )
    return serve_start(bot, update, user_data)


###################
# Block Out Dates #
###################
def bod_start(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("bod_start", user.first_name, msg)
    member_data = admin_collection.get_member(str(user.id))
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    member_block_out_dates_str = latest_block_out_dates.get_member_block_out_dates_str(
        member_name=member_data.get_name()
    )
    options_text, reply_markup = make_options_text_and_reply_markup(
        reply_options_list=[[BLOCK_DATES], [BACK, QUIT]]
    )
    update.message.reply_text(
        text=make_reply_text([member_block_out_dates_str, options_text]),
        reply_markup=reply_markup
    )
    return BLOCK_OUT_DATES_REPLY.get_name()


def bod_reply(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("bod_reply", user.first_name, msg)
    if BLOCK_DATES.reply_check(msg):
        return bod_enter(bot, update, user_data)
    elif BACK.reply_check(msg):
        return serve_start(bot, update, user_data)
    elif QUIT.reply_check(msg):
        return cancel(bot, update)
    else:
        update.message.reply_text(UNKNOWN_REPLY_MSG.get_description(), reply_markup=ReplyKeyboardRemove())
        return bod_start(bot, update, user_data)


def bod_enter(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("block_dates", user.first_name, msg)
    member_data = admin_collection.get_member(str(user.id))
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    member_block_out_dates_str = latest_block_out_dates.get_member_block_out_dates_str(
        member_name=member_data.get_name()
    )
    update.message.reply_text(
        text=make_reply_text([
            member_block_out_dates_str,
            latest_block_out_dates.get_dates_str(),
            ENTER_BLOCK_OUT_DATES_MSG
        ]),
        reply_markup=ReplyKeyboardRemove()
    )
    return BLOCK_OUT_DATES_SUBMIT.get_name()


def bod_submit(bot, update, user_data):
    user, msg = init(bot, update)
    basic_log("block_dates", user.first_name, msg)
    member_data = admin_collection.get_member(str(user.id))
    latest_block_out_dates = block_out_dates_collection.get_latest_block_out_dates()
    if is_valid_bod_input_dates(msg, latest_block_out_dates):
        update.message.reply_text(
            text="Updating Member Block Out Dates",
            reply_markup=ReplyKeyboardRemove()
        )
        typing_action(bot, update)
        latest_block_out_dates.update_member_block_out_dates(
            member_name=member_data.get_name(),
            member_block_out_dates=processed_member_input_block_out_dates(
                msg=msg,
                block_out_dates=latest_block_out_dates
            )
        )
        latest_block_out_dates.update_unconfirmed(member_name=member_data.get_name())
        block_out_dates_collection.update_document(updated_document=latest_block_out_dates)
        update.message.reply_text(
            text="Update Completed\n" + "Returning to Main Menu",
            reply_markup=ReplyKeyboardRemove()
        )
        return serve_start(bot, update, user_data)
    else:
        update.message.reply_text(
            "Invalid Input: {}\n".format(msg) +
            "Please Enter Dates again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return bod_enter(bot, update, user_data)


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


###################################
### Serve Conversation Handler ###
###################################
serve_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(SERVE.get_name(), serve_start, pass_user_data=True)
    ],
    states={
        SERVE_REPLY.get_name(): [
            MessageHandler(Filters.text, serve_reply, pass_user_data=True)
        ],
        ROSTER_REPLY.get_name(): [
            MessageHandler(Filters.text, roster_reply, pass_user_data=True)
        ],
        CREATE_REPLY.get_name(): [
            MessageHandler(Filters.text, create_reply, pass_user_data=True)
        ],
        BLOCK_OUT_DATES_REPLY.get_name(): [
            MessageHandler(Filters.text, bod_reply, pass_user_data=True)
        ],
        BLOCK_OUT_DATES_SUBMIT.get_name(): [
            MessageHandler(Filters.text, bod_submit, pass_user_data=True)
        ],
        CHECK_ROSTER_REPLY.get_name(): [
            MessageHandler(Filters.text, check_roster_reply, pass_user_data=True)
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL.get_name(), cancel)
    ]
)
