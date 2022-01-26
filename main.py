from pydoc import text
from telegram import Update,ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

updater = Updater(token='5084781742:AAE4aq8-Iv_qZHSE2rVW1lvsRwbE5fk1ksw')
job_queue = updater.job_queue

def welcome(update: Update, context: CallbackContext):
    update.message.reply_text(f'Assalomu alaykum {update.effective_user.first_name}, faktbotga xush kelibsiz😊\nFakt izlash uchun /fakt buyrug`ini bosing!')
    add_user_list(update.effective_user.id)

def get_fakt():
    from randfacts import get_fact
    return get_fact()


def fakt(update: Update, context: CallbackContext):
    update.message.reply_text(f'{get_fakt()}\n\nFakt manbasi: @FaktKerakBot')


def stat(update: Update, context: CallbackContext):
    user_list = read_data()
    update.message.reply_text(f'<b>💁🏻 Foydalanuvchilar soni <u>{len(user_list)}</u> ta</b>',parse_mode=ParseMode.HTML)


def new_ads(update: Update, context: CallbackContext):
    text_list = context.args
    text = ''
    for i in  text_list:
        text+=i+' '
    user_list = read_data()
    for user in user_list:
        context.bot.send_message(chat_id=user,text=f'{text}',parse_mode=ParseMode.HTML)


def fakt_job(context):
    context.bot.send_message(chat_id='-1001727951513',text=f'{get_fakt()}\n\n🔍 @FaktKerak',parse_mode=ParseMode.HTML)

job_queue.run_repeating(fakt_job,interval=600.0,first=0.0)


def read_data()->list:
    with open('user_id.txt', 'r', encoding='utf-8') as file:
        lst = file.readlines()
        user_list = []
        for user in lst:
            user_list.append(user.strip())
        return user_list


def check_user_id(user_id):
    user_list = read_data()
    for id in user_list:
        if str(user_id) == str(id):
            return True
    else:
        return False
    

def add_user_list(user_id):
    flag = check_user_id(user_id)
    if not flag:
        with open('user_id.txt', 'a') as file:
            file.write(str(user_id)+'\n')


def error(update: Update, context: CallbackContext):
   update.message.reply_text(f'Fakt izlash uchun iltimos /fakt buyrug`ini bosing!')


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', welcome))
dispatcher.add_handler(CommandHandler('fakt', fakt))
dispatcher.add_handler(CommandHandler('stat', stat))
dispatcher.add_handler(CommandHandler('NewAds', new_ads))
dispatcher.add_handler(MessageHandler(Filters.all, error))

updater.start_polling()
updater.idle()
