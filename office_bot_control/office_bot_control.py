#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import os
import subprocess
#import telepot
from subprocess import STDOUT, check_output
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def temperature():
    p = subprocess.Popen("timeout 1 mosquitto_sub -h 10.32.21.35 -t temperature -u changlin -P qwe456uio", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    tem = str(p)
    tem = tem.strip("b")
    tem = tem.strip("'")
    tem = tem.strip("n")
    tem = tem.strip("\\")
    return "The inside temperature is: "+tem+" degree of C"
def temperature_out():
    p = subprocess.Popen("timeout 1 mosquitto_sub -h 10.32.21.35 -t temperature_out -u changlin -P qwe456uio", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    tem = str(p)
    tem = tem.strip("b")
    tem = tem.strip("'")
    tem = tem.strip("n")
    tem = tem.strip("\\")
    return "The outside temperature is: "+tem+" degree of C"

def rain():
    p = subprocess.Popen("timeout 1 mosquitto_sub -h 10.32.21.35 -t rain -u changlin -P qwe456uio", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    r = str(p)
    r = r.strip("b")
    r = r.strip("'")
    r = r.strip("n")
    r = r.strip("\\")
    if r == '0':
        return "Now is raining!"
    else:
        return "Shining now!"
def switch(input):

    if input == 'O':
        os.system('timeout 1 mosquitto_pub -t switch -m '+input+' -u changlin03 -P qwe456uio')
    elif input == 'F': 
        os.system('timeout 1 mosquitto_pub -t switch -m '+input+' -u changlin03 -P qwe456uio')
def switch_auto(input):
    if input == 'O':
        os.system('timeout 1 mosquitto_pub -t auto_switch -m '+input+' -u changlin03 -P qwe456uio')
    elif input == 'F':
        os.system('timeout 1 mosquitto_pub -t auto_switch -m '+input+' -u changlin03 -P qwe456uio')
                

def check_id(self,msg):
    content_type, chat_type, chat_id = telepot.glance(msg)


def start(update: Update, context: CallbackContext) -> None:
    
    keyboard1 = [
            [
            InlineKeyboardButton("Inside temperature",callback_data=temperature()),
        ],
            [
            InlineKeyboardButton("Switch_auto On",callback_data="Switch_auto on!"),
            InlineKeyboardButton("Switch_auto Off",callback_data="Switch_auto off!"),
        ],

            [
            InlineKeyboardButton("Switch On",callback_data="Air-con on! Please press Switch_auto On first if not work"),
            InlineKeyboardButton("Switch Off",callback_data="Air-con off! Please press Switch_auto On first if not work"),
        ],
            [
            InlineKeyboardButton("Outside temperature",callback_data=temperature_out()),
            InlineKeyboardButton("Rain_or_Not",callback_data=rain()),
        ]

    ]
    keyboard2 = [
            [
            InlineKeyboardButton("Outside temperature",callback_data=temperature_out()),
            InlineKeyboardButton("Rain_or_Not",callback_data=rain()),
        ]
    ]



    if update.message.chat.id == 1021794628:

        reply_markup = InlineKeyboardMarkup(keyboard1)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard2)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Air-con on! Please press Switch_auto On first if not work":
        switch('O')
    elif query.data == "Air-con off! Please press Switch_auto On first if not work":
        switch('F')
    if query.data == "Switch_auto on!":
        switch_auto('O')
    elif query.data == "Switch_auto off!":
        switch_auto('F')


    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1351667509:AAEuwMsB9mLuhWGuWzaT0eOadVMXU_hGXss", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
