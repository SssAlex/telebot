#!/usr/bin/python

from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_params(method_name, update):
    logger.debug("Method: %s\nFrom: %s\nchat_id: %d\nText: %s" %
                 (method_name,
                  update.message.from_user,
                  update.message.chat_id,
                  update.message.text))


ACCESS_TOKEN = ''


def start(bot, update):
    help(bot, update)


def confirmAction(bot, update):
    pass


def button(bot, update):
    keyboard = [[InlineKeyboardButton(text="Confirm", callback_data='Yes'), InlineKeyboardButton(text="Reject", callback_data='No')]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Are you sure?:', reply_markup=reply_markup)


def help(bot, update):
    # log_params('help', update)
    bot.sendMessage(update.message.chat_id,
                    text="""Supported commands:

                    \t/button - for tests

                    \t/help - show list of commands
                    \t/serverStatus - show server status
                    \t/reboot - reboot server""")


def serverStatus(bot, update):
    # log_params('help', update)
    subprocess.run(["uptime"])
    bot.sendMessage(update.message.chat_id, text='')
    pass


def reboot(bot, update):
    # log_params('help', update)
    if confirmAction(bot, update) is True:
        subprocess.run(["ls", "-l"])
    else:
        pass


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(ACCESS_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("serverStatus", serverStatus))
    dp.add_handler(CommandHandler("button", button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
