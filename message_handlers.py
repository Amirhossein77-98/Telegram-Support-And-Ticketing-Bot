from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from checkers import *
import database_manager
import config
from config import bot_warnings
import functions

async def reply(update: Update, context: CallbackContext):

    current_user_id = update.message.from_user.id
    
    if current_user_id in config.admin_id:
        try:
            bot_forwarded_messages_id = context.user_data["msg_id_list"]

            reply_to_message_id = update.message.reply_to_message.message_id

            if reply_to_message_id in bot_forwarded_messages_id:
                message_index_id = bot_forwarded_messages_id.index(reply_to_message_id)
            
            history = context.user_data["history"]
            
            if 0 <= message_index_id <= len(history):
                # Get the original message_id from the history list
                original_message_id = int(history[message_index_id][0])
            else:
                # Handle the case when the admin did not reply to a message from the history list
                # For example, send a message to the admin asking them to reply to a message from the history list
                await update.message.reply_text(bot_warnings['choose_correct_message'])
                return

            user_id = context.user_data['reply_to']
            # if "reply_to" in context.user_data:
            #     user_id = context.user_data['reply_to']
            # else:
            #     user_id = admin_id[0]

            await context.bot.send_message(chat_id=user_id, text=update.message.text, reply_to_message_id=original_message_id)
            await update.message.reply_text(bot_warnings['approve_sent_message'])

            users_name = context.user_data["users_first_name"]
            message_id = update.message.message_id
            message_text = update.message.text
            database_manager.db.save_admin_replied_messages(user_id, users_name, original_message_id, current_user_id, message_id, message_text)
        
        except KeyError:
            await update.message.reply_text(bot_warnings['weak_mind'])


    else:
        message_text = update.message.text
        replying_message_text = update.message.reply_to_message.text
        user_id = update.message.from_user.id
        users_name = update.message.from_user.first_name
        message_id = update.message.message_id
        message_date = update.message.date
        date_str = functions.convert_time(message_date)

        message_data = database_manager.db.admin_replied_message_index_to_a_specific_users_message(user_id, replying_message_text)
        admin_id = message_data[0]
        admin_message_index = message_data[1]

        database_manager.db.save_message(user_id, user_id, users_name, message_text, message_id, date_str, admin_message_index, admin_id)
        await update.message.reply_text(text_messages['approve_user_message_sent_to_support_team'])


async def message(update: Update, context: CallbackContext) -> None:
    """Echo the user's message and save it"""
    user_id = update.message.from_user.id

    if is_blocked(user_id):
        await update.message.reply_text(text_messages['youre_blocked'])
        return

    if not await require_subscription(update, context):
        return
    
    if user_id in admin_id:
        await update.message.reply_text(bot_warnings['undefined_admin_message'])
        return

    chat_id = update.message.chat.id
    user_name = update.message.from_user.first_name
    message = update.message.text
    message_id = update.message.message_id
    message_date = update.message.date
    date_str = functions.convert_time(message_date)
    reply_id = 0

    
    database_manager.db.save_message(chat_id, user_id, user_name, message, message_id, date_str, reply_id, 0)

    await update.message.reply_text(text_messages['approve_user_message_sent_to_support_team'])
    for admin in config.admin_id:
        await context.bot.send_message(chat_id=admin, text=text_messages['new_message_notification'].format(user_name))