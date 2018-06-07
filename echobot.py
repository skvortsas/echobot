from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import re
import json


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
IDs = []
url = 'https://e.nariman.io/events'
api = requests.get(url)
All_events_ID = []
All_events_Names = []


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    global  api
    global All_events_ID
    global All_events_Names
    update.message.reply_text("Let's roll")
    data = json.loads(api.text)
    for event in data['data']:
        All_events_ID.append(event['id'])
        All_events_Names.append(event['name'])
        update.message.reply_text(All_events_ID)
        update.message.reply_text(All_events_Names)

def get_all_events(bot, update):
    """To get all the events"""
    global api
    data = json.loads(api.text)
    for event in data['data']:
       update.message.reply_text(event['id'])

def add_event(bot, update):
    """Add an event into ids to get it back later"""
    global IDs
    global All_events
    the_id = re.search('(?<=\/add\_event\s).+', update.message.text)
    if All_events.count(the_id.group()) > 0:
        if IDs.count(the_id.group()) < 1:
            IDs.append(the_id.group())
            update.message.reply_text('We added your ID: "'+ the_id.group() +'"')
        else:
            update.message.reply_text("you already have this ID")
    else:
        update.message.reply_text("your ID does not exist")

def del_event(bot, update):
    """Delete an event in the list of the IDs"""
    global IDs
    the_id = re.search('(?<=\/del\_event\s).+', update.message.text)
    if IDs.count(the_id.group()) > 0:
        IDs.remove(the_id.group())
        update.message.reply_text('We removed the ID: "'+ the_id.group() +'" from your list')
    else:
        update.message.reply_text("There is no such ID")

def list(bot, update):
    """To get the list of the IDs the user have"""
    global IDs
    update.message.reply_text(IDs)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('These are our commands:\n/start: to roll with us'
                              '\n/help: to get to this selection'
                              '\n/add_event: to add an event you want to visit'
                              '\n/del_event: to remove an event you dont want to visit any more, or youve visited it already'
                              '\n/list: to get the list of your events you want to visit'
                              '\n/get_all_events: to see the list of all events')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text('type: /help to know more')


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
    dp.add_handler(CommandHandler("del_event", del_event))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("get_all_events", get_all_events))

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