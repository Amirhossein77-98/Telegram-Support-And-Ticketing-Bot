Telegram Support Bot
This is a Telegram bot built using python-telegram-bot library to provide a support ticketing system.

Features
Users can message the bot to create a ticket
Admins can view and reply to user tickets in the inbox
Admins can block users
Message history stored in SQLite database
Users must join a channel before accessing bot
Usage
Users
Message the bot to create a ticket
Use /start to initialize bot
Must join configured channel before accessing bot
Admins
/inbox - View list of users with tickets
/block - Block a user
/manage_users - Menu to block/delete users
Reply to message in inbox thread to respond to user
Setup
Clone repo
Create virtualenv
Install dependencies from requirements.txt
Configure config.py with bot token and admin IDs
Run python main.py to start bot
Architecture
main.py - Initializes bot and registers handlers
config.py - Bot configuration and constants
database_manager.py - SQLite database helper functions
handlers/ - Bot command and callback handlers
utils/ - Reusable helper functions
License
This project is licensed under the MIT License - see the LICENSE file for details.

Let me know if you would like any sections expanded or have additional questions!