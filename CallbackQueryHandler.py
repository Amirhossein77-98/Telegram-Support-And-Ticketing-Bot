from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from telegram.constants import ParseMode
import database_manager
from functions import show_delete_users, show_unblock_users
from config import text_messages, bot_warnings

def message_structure(message_date, message_time, message):
    return f"""
📅 Date: {message_date} Time: {message_time}

💬 Message: {message}
"""

def save_to_context(context ,user_id, users_name, msg_id_list):
    context.user_data['reply_to'] = user_id
    context.user_data["users_id"] = user_id
    context.user_data["users_first_name"] = users_name
    context.user_data["msg_id_list"] = msg_id_list


async def button_pressed(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    
    if query.data.startswith("msg"):
        user_id = int(query.data.split("-")[1])
        users_name = database_manager.db.get_users_name(user_id)
        linked_name = f'<a href="tg://user?id={user_id}">{users_name[0]}</a>'

        history = database_manager.db.get_user_messages(user_id)
        context.user_data["history"] = history

        message_availible_to_show = False
        msg_id_list = []
        full_history_button = [[InlineKeyboardButton(f"Complete message history of {users_name[0]}", callback_data='fhmsg-' + str(user_id))]]
        reply_markup = InlineKeyboardMarkup(full_history_button)
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"⏮️ New messages of {linked_name}: \n⛔ Block the user: /block", parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        for msg in history:
            if msg[5] == 0:
                if msg[6] == None:
                    message_date = msg[1].split(" ")[0]
                    message_time = msg[1].split(" ")[1]
                    message = message_structure(message_date, message_time, msg[4])

                    if msg[2] == "0":
                        sent_msg = await context.bot.send_message(chat_id=query.message.chat_id, text=message)
                        message_availible_to_show = True
                    else:
                        await context.bot.send_message(chat_id=query.message.chat_id, text=message, reply_to_message_id=int(msg[2]))
                        message_availible_to_show = True
                    
                    msg_id_list.append(sent_msg.message_id)

                    database_manager.db.update_message_read_state(user_id, msg[0])
                elif msg[6] != None:
                    message_date = msg[1].split(" ")[0]
                    message_time = msg[1].split(" ")[1]
                    img_url = f'images/{user_id}/photo_{msg[6]}.jpg'
                    message = message_structure(message_date, message_time, msg[4])

                    if msg[2] == "0":
                        sent_msg = await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(img_url, 'rb'), caption=message)
                        message_availible_to_show = True
                    else:
                        await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(img_url, 'rb'), reply_to_message_id=int(msg[2]))
                        message_availible_to_show = True
                    
                    msg_id_list.append(sent_msg.message_id)

                    database_manager.db.update_message_read_state(user_id, msg[0])

        if message_availible_to_show == False:
            sent_msg = await context.bot.send_message(chat_id=query.message.chat_id, text=bot_warnings['all_messages_read'])

        save_to_context(context=context, user_id=user_id, users_name=users_name[0], msg_id_list=msg_id_list)
    
    if query.data.startswith("fhmsg"):
        user_id = int(query.data.split("-")[1])
        users_name = database_manager.db.get_users_name(user_id)
        linked_name = f'<a href="tg://user?id={user_id}">{users_name[0]}</a>'

        history = database_manager.db.get_user_messages(user_id)
        context.user_data["history"] = history

        msg_id_list = []
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"⏮️ Complete message history of {linked_name}: \n⛔ Block user: /block", parse_mode=ParseMode.HTML)
        for msg in history:
            if msg[6] == None:
                message_date = msg[1].split(" ")[0]
                message_time = msg[1].split(" ")[1]
                message = message_structure(message_date, message_time, msg[4])

                if msg[2] == "0":
                    sent_msg = await context.bot.send_message(chat_id=query.message.chat_id, text=message)
                    message_availible_to_show = True
                else:
                    await context.bot.send_message(chat_id=query.message.chat_id, text=message, reply_to_message_id=int(msg[2]))
                    message_availible_to_show = True
                
                msg_id_list.append(sent_msg.message_id)

                database_manager.db.update_message_read_state(user_id, msg[0])
            elif msg[6] != None:
                message_date = msg[1].split(" ")[0]
                message_time = msg[1].split(" ")[1]
                img_url = f'images/{user_id}/photo_{msg[6]}.jpg'
                message = message_structure(message_date, message_time, msg[4])

                if msg[2] == "0":
                    sent_msg = await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(img_url, 'rb'), caption=message)
                    message_availible_to_show = True
                else:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(img_url, 'rb'), reply_to_message_id=int(msg[2]))
                    message_availible_to_show = True
                
                msg_id_list.append(sent_msg.message_id)

                database_manager.db.update_message_read_state(user_id, msg[0])

        save_to_context(context=context, user_id=user_id, users_name=users_name[0], msg_id_list=msg_id_list)

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