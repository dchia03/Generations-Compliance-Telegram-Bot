from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import Updater

from main.conversation.administration_conversation import admin_conv_handler
from main.conversation.feedback_conversation import feedback_conv_handler
from main.conversation.serve_conversation import serve_conv_handler
from main.stores.database_store import admin_db
from main.utils.logger import Logger
from properties import props

log = Logger(__name__)


######################
## Helper Functions ##
######################
def get_all_members_ids():
    all_ids = []
    all_admin_data = admin_db.collection.find({})
    for data in all_admin_data:
        all_ids.append(int(data["Telegram ID"]))
    return all_ids


def get_ministry_head_id():
    all_admin_data = admin_db.collection.find({})
    for data in all_admin_data:
        if data["Role"] == "Ministry Head":
            return int(data["Telegram ID"])
    return 0


def send_update_message_to_all(updater):
    update_msg_template = "Generations Compliance Telegram Bot Update\n\n"
    update_msg_content = "Added Replace Duty Feature.\n" \
                         + "Members can now request a replace of duty through the telegram bot"
    update_msg = update_msg_template + update_msg_content
    for id in get_all_members_ids():
        updater.bot.send_message(
            chat_id=int(id),
            text=update_msg
        )


def send_update_message_test_to_admin(updater):
    update_msg = "THIS IS A TEST"
    if get_ministry_head_id() != 0:
        updater.bot.send_message(
            chat_id=get_ministry_head_id(),
            text=update_msg
        )
    else:
        print("CANNOT FIND ADMIN")


#######################################
## Additional Conversation Functions ##
#######################################
def error(bot, update, err):
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, err)
    update.message.reply_text(
        'Connection Timed Out\n' +
        'Resetting Connection\n' +
        'Please Type /cancel and restart'
    )


def cancel(bot, update):
    user = update.message.from_user
    log.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Session Ended",
        reply_markup=ReplyKeyboardRemove()
    )



log.info("Profile: " + props.profile)
generations_compliance_bot_token = props.chatbot_token
updater = Updater(token=generations_compliance_bot_token)
# send_update_message_to_all(updater = updater)
dp = updater.dispatcher
dp.add_handler(admin_conv_handler)
dp.add_handler(serve_conv_handler)
dp.add_handler(feedback_conv_handler)
dp.add_handler(CommandHandler("Cancel", cancel))
dp.add_error_handler(error)
updater.start_polling()
log.info("Bot Started")
updater.idle()