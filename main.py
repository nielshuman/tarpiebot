AUTHORIZED_USERS = [5964123828]

import telebot
import os
import time
from dotenv import load_dotenv
import subprocess
load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
location = os.getenv('DOWNLOAD_LOCATION')
def is_authorized(message):
    return message.from_user.id in AUTHORIZED_USERS

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: message.text.startswith('https://open.spotify.com/track/'))
def echo_all(message):
    if not is_authorized(message):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return
    download_process = subprocess.Popen(['python3', '-m', 'spotdl', message.text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=location)
    bot.reply_to(message, "Downloading...")
    for line in download_process.stdout:
        line = line.decode('utf-8')
        if 'Processing query' in line:
            continue
        # remove everything after 'https://'
        if ': https://' in line:
            line = line.split(': https://')[0]
        if line.strip() != '':
            bot.send_message(message.chat.id, line)
        if 'An error occurred' in line:
            break
bot.infinity_polling()