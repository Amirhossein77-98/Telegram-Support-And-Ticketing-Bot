from telegram import Update, ChatMember
from telegram.ext import CallbackContext
import database_manager as db
from config import *

async def check_user_access(user_id):
    if user_id in admin_id:
        return True
    else:
        return False

def is_blocked(user_id):
    result = db.db.block_checker(user_id)
    return result > 0

async def require_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
    except TelegramError as e:
        print(e)
        return False

    if member.status != ChatMember.MEMBER and member.status != ChatMember.ADMINISTRATOR and member.status != ChatMember.OWNER:
        await update.message.reply_text(bot_warnings['join_channel'])
        return False
    else:
        return True