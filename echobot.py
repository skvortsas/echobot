from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
import config
import logging
import requests
import re
import json


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
MENU, INFO = range(2)
logger = logging.getLogger(__name__)
url = 'https://e.nariman.io/events'
api = ""
api = requests.get(url)
IDs = []
All_events_ID = []
All_events_Names = []
n = step_event_list = 3
current_page = 1
count_message_del = 0
i = 0
user_chat_id = ""
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    global user_chat_id
    reply_keyboard = [['event list'], ['add event'], ['my events']]
    user_chat_id = update.message.chat_id
    print(user_chat_id)
    update.message.reply_text(
        'Выберите одну из команд\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return MENU

def event_list(bot, update):
    global n
    global count_message_del
    global i
    global user_chat_id
    n = step_event_list * current_page
    keyboard = [[],[]]
    if(current_page == 1):
        get_event_ID_Names()
    i = len(All_events_ID)
    if n < i:
        for k in range(n-step_event_list, n):
            if(k == n-1):
                keyboard[0].append((InlineKeyboardButton(k+1, callback_data=All_events_ID[k])))
                keyboard[1].append((InlineKeyboardButton('<-', callback_data="previous")))
                keyboard[1].append((InlineKeyboardButton('->', callback_data="next")))
                reply_markup = InlineKeyboardMarkup(keyboard)
                count_message_del = step_event_list
                print("count" + str(count_message_del))
                bot.send_message(chat_id=user_chat_id, text=str(k+1) + " " + All_events_Names[k], reply_markup=reply_markup)

            else:

                bot.send_message(chat_id=user_chat_id, text=str(k+1) + " " + All_events_Names[k])
                keyboard[0].append((InlineKeyboardButton(k+1, callback_data=All_events_ID[k])))

    else:
        for k in range(n-step_event_list, i):
            if(k == i-1):
                keyboard[0].append((InlineKeyboardButton(k+1, callback_data=All_events_ID[k])))
                reply_markup = InlineKeyboardMarkup(keyboard)
                keyboard[1].append((InlineKeyboardButton('<-', callback_data="previous")))
                keyboard[1].append((InlineKeyboardButton('->', callback_data="next")))
                count_message_del =step_event_list -  (n - i)
                print("cout" +  str(count_message_del))
                bot.send_message(chat_id=user_chat_id, text=str(k+1) + " " + All_events_Names[k],reply_markup=reply_markup)
            else:
                bot.send_message(chat_id=user_chat_id, text=str(k+1) + " " + All_events_Names[k])
                keyboard[0].append((InlineKeyboardButton(k+1, callback_data=All_events_ID[k])))

def button(bot, update):
    query = update.callback_query
    global current_page
    for k in range(count_message_del):
        bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id-k)
    if(query.data == "previous"):
        if(current_page == 1):
            tmp = divmod(i, step_event_list)
            if(tmp[1] == 0):
                current_page = tmp[0]
            else:
                current_page = tmp[0] + 1
        else:
            current_page-=1
        event_list(bot, update)

    elif(query.data == "next"):
        if(current_page * step_event_list > i):
            current_page = 1
        else:
            current_page+=1
        event_list(bot, update)
    else:
        reply_keyboard = [['sign up'], ['back']]
        bot.send_message(chat_id=query.message.chat_id, text=get_info(query.data),reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

def sign_up(bot, update):
    update.message.reply_text("Я еще не сделал")
    start(bot, update)

def back(bot, update):
    event_list(bot, update)

def get_info(ID):
    global api
    data = json.loads(api.text)
    tmp = All_events_ID.index(ID)
    description = data['data'][tmp]['description']
    return description

def get_event_ID_Names():
    api = requests.get(url)
    data = json.loads(api.text)
    All_events_ID.clear()
    All_events_Names.clear()
    for event in data['data']:
        All_events_ID.append(event['id'])
        All_events_Names.append(event['name'])

def add_event(bot, update):
    """Add an event into ids to get it back later"""
    global IDs
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
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [RegexHandler('start', start)],
            MENU: [RegexHandler('event list', event_list)],
            #MENU: [RegexHandler('add event', )],
            #MENU: [RegexHandler('my events',)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)








    dp.add_handler(CallbackQueryHandler(button))
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add_event", add_event))
    dp.add_handler(CommandHandler("del_event", del_event))
    dp.add_handler(CommandHandler("list", list))



    # handlers for button
    dp.add_handler(RegexHandler("sign up", sign_up))
    dp.add_handler(RegexHandler("back", back))


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
