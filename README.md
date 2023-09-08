**Telegram Support and Ticketing Bot**

This is a Telegram bot built using python-telegram-bot V20.4 library to provide a supporting and ticketing system bot.

**Features**
- Users can message the bot to create a ticket or chat with the support team
- Admins can view and reply to user tickets in the inbox and the message will be replied in user's chat
- Admins can block/unblock users
- Admins can delete chat histories
- Message history stored in SQLite database
- Users must join a channel before accessing bot

**Usage**
# Users
- Must join configured channel before accessing bot
- Use /start to initialize bot
- Message the bot to create a ticket

# Admins
- /inbox - View list of users with tickets and see each user's message history by tapping on their name's button
- Reply to message in inbox thread to respond to user
- /block - Block that user whose chat history is in view
- /manage_users - Menu to unblock/delete users

**Setup**
- Clone repo
- Create virtualenv (optional)
- Install dependencies from requirements.txt. Most of the time installing python-telegram-bot and pytz is enough
- Configure config.py with bot token, admin IDs, and channel username.
- Modify message texts to your own desire if required
- Run python main.py to start bot

**Architecture**
- main.py - Initializes bot and registers handlers
- config.py - Bot configuration and constants
- database_manager.py - SQLite database helper functions
- handlers/ - Bot command and callback handlers
- utils/ - Reusable helper functions
