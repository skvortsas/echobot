from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import re
from telegram import ReplyMarkup


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
IDs = []
url = 'https://e.nariman.io/events'


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Let's roll")

def add_event(bot, update):
    """Add an event into ids to get it back later"""
    update.message.reply_text("Give the ID of the event you want to add")
    update.message.ForceReply("kekas")


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('These are our commands:')


def echo(bot, update):
    """Echo the user message."""
    global IDs
    api = requests.get(url)
    all_ids = re.findall(r'(?<=id\"\:\").+?(?=\")', api.text)
    update.message.reply_text(all_ids)
    update.message.reply_text(IDs)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("521686995:AAGmtSwu2OguklgQnGbaiHAsliAgLQ7Tm94")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add_event", add_event))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()