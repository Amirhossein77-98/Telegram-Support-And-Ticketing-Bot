from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from checkers import check_user_access, require_subscription
import database_manager
from config import admin_id, text_messages, commands_texts, buttons_texts

async def block(update, context):
    if not await check_user_access(update.message.from_user.id):
        return
    
    user_id = context.user_data['users_id']
    users_first_name = context.user_data['users_first_name']
    
    database_manager.db.add_user_to_blocklist(user_id, users_first_name)
    
    await update.message.reply_text(text_messages['user_blocked'])

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if not await require_subscription(update, context):
        return
    
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    database_manager.db.save_user(user_id, user_name)

    if user_id not in admin_id:
        await update.message.reply_text(text_messages['user_start'].format(user_name))
        return
    
    await update.message.reply_text(text_messages['admin_start'])


async def inbox(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show inbox menu"""

    if update.callback_query:
        return
  
    if not await check_user_access(update.message.from_user.id):
        await update.message.reply_text(text_messages['access_denied'])
        return

    users = database_manager.db.get_user_list()

    buttons = []
    for user in users:
        button = InlineKeyboardButton(user[1], callback_data='msg-' + user[0])
        row = [button]
        buttons.append(row)

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(commands_texts['select_user'], reply_markup=reply_markup)
    return
async def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if not await require_subscription(update, context):
        return

    await update.message.reply_text(text_messages['help'])

async def bot_stats(update: Update, context: CallbackContext) -> None:
    if not await check_user_access(update.message.from_user.id):
        await update.message.reply_text(text_messages['access_denied'])
        return

    users_count = database_manager.db.count_users()
    await update.message.reply_text(f"{commands_texts['bot_users_count']} {users_count}")
    
async def manage_users(update: Update, context: CallbackContext) -> None:
    if not await check_user_access(update.message.from_user.id):
        await update.message.reply_text(text_messages['access_denied'])
        return

    buttons = [
        [InlineKeyboardButton(buttons_texts['delete_user'], callback_data="delete")],
        [InlineKeyboardButton(buttons_texts['unblock_user'], callback_data="unblock")]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(commands_texts['what_to_do_with_users'], reply_markup=keyboard)