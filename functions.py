import datetime
import config
import pytz
import database_manager
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes

def convert_time(message_date):
    timezone = pytz.timezone(config.timezone)
    msg_date_tehran = message_date.astimezone(timezone)
    date_str = msg_date_tehran.strftime("%Y-%m-%d %H:%M:%S")
    return date_str

async def show_delete_users(update, context):

    users = database_manager.db.get_user_list()

    buttons = []

    for user in users:
        buttons.append([InlineKeyboardButton(user[1], callback_data=f"delete-{user[0]}")])

    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query

    await query.edit_message_text(text=config.commands_texts['choose_someone_to_delete'], reply_markup=keyboard)

async def show_unblock_users(update, context):

    users = database_manager.db.get_blocked_user_list()
    
    buttons = []

    for user in users:
        buttons.append([InlineKeyboardButton(user[1], callback_data=f"unblock-{user[0]}")])

    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query

    await query.edit_message_text(text=config.commands_texts['choose_someone_to_unblock'], reply_markup=keyboard)