#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import json
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app import get_current_currency, BadResponse, sleep, CURRENCIES
import requests
from src.find_profit_list import find_profit_list

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    current_user = update.message.from_user.id

    with open("users.json", "r") as f:
        users = set(json.load(f))

    if current_user not in users:
        users.add(current_user)

    with open("users.json", "w") as f:
        json.dump(list(users), f)

    update.message.reply_text("Привет!\nТеперь ты подписан на рассылку!")


def echo(update, context):
    """Echo the user message."""
    logger.info(update.message.from_user.id)
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def send_signals(updater, currencies):
    with open("users.json", "r") as f:
        subscribed_users = json.load(f)

    for user in subscribed_users:
        updater.bot.sendMessage(chat_id=str(user), text=str(currencies))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "5238631123:AAH465nhVGKN-OcBoIF-Z6avkHwiwP9pKWU", use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    while True:

        try:

            print("TEST HACK")
            actual_curs = get_current_currency()
            profit_list = find_profit_list(actual_curs, CURRENCIES)
            if profit_list:
                send_signals(updater=updater, currencies=profit_list)

        except requests.exceptions.Timeout:
            print("Timeout Error")
        except BadResponse:
            print("Bad Response")

        sleep()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == "__main__":
    main()
