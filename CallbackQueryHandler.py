from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from telegram.constants import ParseMode
import database_manager
from functions import show_delete_users, show_unblock_users
from config import text_messages

async def button_pressed(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    
    if query.data.startswith("msg"):
        user_id = int(query.data.split("-")[1])
        users_name = database_manager.db.get_users_name(user_id)
        linked_name = f'<a href="tg://user?id={user_id}">{users_name[0]}</a>'

        history = database_manager.db.get_user_messages(user_id)
        context.user_data["history"] = history

        msg_id_list = []
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"⏮️ Messsage history from {linked_name}: \n⛔ Block the user: /block", parse_mode=ParseMode.HTML)
        for msg in history:
            message_date = msg[1].split(" ")[0]
            message_time = msg[1].split(" ")[1]
            message = f"""
📅 Date: {message_date}, Time: {message_time}

💬 Message: {msg[4]}
"""
            if msg[2] == "0":
                sent_msg = await context.bot.send_message(chat_id=query.message.chat_id,
                                                text=message)
            else:
                await context.bot.send_message(chat_id=query.message.chat_id, text=message, reply_to_message_id=int(msg[2]))
            msg_id_list.append(sent_msg.message_id)

        context.user_data['reply_to'] = user_id
        context.user_data["users_id"] = user_id
        context.user_data["users_first_name"] = users_name[0]
        context.user_data["msg_id_list"] = msg_id_list

    if query.data.startswith("delete-"):
        user_id = int(query.data.split("-")[1])
        database_manager.db.delete_user_history(user_id)

        await context.bot.send_message(chat_id=query.message.chat_id, text=text_messages['user_delete_successful'])

    if query.data.startswith("unblock-"):
        user_id = int(query.data.split("-")[1])
        database_manager.db.unblock_user(user_id)

        await context.bot.send_message(chat_id=query.message.chat_id, text=text_messages['user_unblock_successful'])

    if query.data == "delete":
        await show_delete_users(update, context)

    if query.data == "unblock":
        await show_unblock_users(update, context)