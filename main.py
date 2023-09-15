import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger('TGDBBOT-LOGGER')

from datetime import datetime 
import pathlib
import json
import re

import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

from typing import List, Union, Optional

from telethon import Button
from telethon.sync import TelegramClient, events


WORK_IN_PROGRESS = 'WIP'
TODAY = datetime.today().strftime('%Y%m%d')
actions = ['GET', 'UPDATE', 'INSERT', 'DELETE']
buttons_actions = [Button.inline(x) for x in actions]

# Use your own values from my.telegram.org
API_ID = config['Telegram']['API_ID']
API_HASH = config['Telegram']['API_HASH']
BOT_TOKEN = config['Telegram']['BOT_TOKEN']
session_name = 'sessions/Bot'
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = f"Hi {sender.username}\n" + "CRUD Bot 🤖 ready\n" +\
        "I can perform CRUD operation for you!\n"+\
        "You can add/update/get/delete rows from two tables:\n"+\
        "\"<b>Clients</b>\n"+\
        "\"<b>Orders</b>\n"+\
        "Make your choice!"
    await client.send_message(
        SENDER, 
        text,
        parse_mode="HTML",
        buttons=[
            Button.inline('Clients'),
            Button.inline('Orders')
        ])
    
@client.on(events.NewMessage(pattern="(?i)/clear"))
async def clear(event):
    await start(event)

@client.on(events.CallbackQuery(data=b'Orders'))
async def handlerStart(event):
    sender = await event.get_sender()
    SENDER = sender.id
    await client.send_message(SENDER, 'Which actions can you perform?', 
                        buttons=buttons_actions)


    
@client.on(events.CallbackQuery(data=b'Clients'))
async def handlerStart(event):
    sender = await event.get_sender()
    SENDER = sender.id
    await client.send_message(SENDER, 'Which actions can you perform?', 
                        buttons=buttons_actions)
    @client.on(events.CallbackQuery(data=b'GET'))
    async def handlerGet(event):
        sender = await event.get_sender()
        SENDER = sender.id
        await client.send_message(
                SENDER,
                'GET METHOD'
            )
    @client.on(events.CallbackQuery(data=b'UPDATE'))
    async def handlerGet(event):
        sender = await event.get_sender()
        SENDER = sender.id
        await client.send_message(
                SENDER,
                'GET METHOD'
            )
    @client.on(events.CallbackQuery(data=b'DELETE'))
    async def handlerGet(event):
        sender = await event.get_sender()
        SENDER = sender.id
        await client.send_message(
                SENDER,
                'GET METHOD'
            )
    @client.on(events.CallbackQuery(data=b'INSERT'))
    async def handlerGet(event):
        sender = await event.get_sender()
        SENDER = sender.id
        await client.send_message(
                SENDER,
                'GET METHOD'
            )
    


if __name__ == '__main__':
    print(client.is_connected())
    print(client.get_me())
    print(client.is_bot())
    client.run_until_disconnected()