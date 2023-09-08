from config import bot_token #Importing config.py to access bot token and other configs
from command_handlers import * #Importing all command handlers to manage them
from message_handlers import * #Importing all message handlers to manage them
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler #Importing all required libraries from telegram extensions
import logging #Importing logger library to log everything
from CallbackQueryHandler import button_pressed

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Defining application and command handlers, message handlers, callback query handlers, and starting the bot
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # Adding Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("inbox", inbox))
    application.add_handler(CommandHandler("block", block))
    application.add_handler(CommandHandler("manage_users", manage_users))
    application.add_handler(CommandHandler("bot_stats", bot_stats))
    application.add_handler(CommandHandler("help", help))
    # Adding Message Handlers
    application.add_handler(MessageHandler(filters.REPLY, reply))
    application.add_handler(MessageHandler(filters.TEXT, message))
    # Adding CallbackQuery Handlers
    application.add_handler(CallbackQueryHandler(button_pressed))

    # Start the Bot
    application.run_polling(1.0)


if __name__ == '__main__':
    main()