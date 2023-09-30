# Database Info
DB_FILE = "data.db"

# Admin and channel info
channel_id = "@channel_id"
admin_id = ['admin ID(s) --> int'] # Allowed user IDs

# Bot Settings
bot_token = "BOT-TOKEN"

# App Settings
timezone = 'Asia/Tehran'

# Messages
text_messages = {
    'user_start': 'Hi {}, I am a support bot. You can send me a message and I will send it to the support team😊.',
    'admin_start': 'Hi dear admin. How can I help you?',
    'access_denied': "Sorry, but you don't have access to this bot.",
    'help': 'Use /start to get started. Send me a message and I will forward it to support. Use /inbox to see your messages. Support can reply using /reply your_id.',
    'approve_user_message_sent_to_support_team': 'Thanks for your message. your message has been sent to the support team. I will forward their response to you whenever they reply.',
    'youre_blocked': 'Sorry but you are blocked and you can\'t use this bot.',
    'user_delete_successful': 'User deleted successfully',
    'user_unblock_successful': 'User unblocked successfully',
    'user_blocked': 'User blocked successfully',
    'new_message_notification': 'You have a new message from {}.',
}

commands_texts = {
    'select_user': 'Select what you wanna do please:',
    'bot_users_count': 'Bot users count:',
    'what_to_do_with_users': 'What you wanna do with users:',
    'choose_someone_to_delete': 'Please choose someone to delete. Be causious to not delete wrong user.',
    'choose_someone_to_unblock': 'Please choose someone to unblock.',
}

buttons_texts = {
    'delete_user': 'Delete User',
    'unblock_user': 'Unblock User',
}

bot_warnings = {
    'choose_correct_message': 'Please reply to a message of the user.',
    'approve_sent_message': 'Message sent to the user.',
    'weak_mind': 'Sorry I lost the message, Please send /inbox again and choose user to reply to their message.',
    'undefined_admin_message': 'I don\'t know what to do with this message. Please reply to a user\'s message or use commands.',
    'join_channel': 'Please join our channel first to use this bot.\n\n@channel_id',
    'all_messages_read': 'There is no Unred message from this user. If you want to see their chat history click on the button above👆'
}