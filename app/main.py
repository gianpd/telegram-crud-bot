import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger('TGDBBOT-LOGGER')

from datetime import datetime 

import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

from typing import List, Union, Optional

from telethon import Button
from telethon.sync import TelegramClient, events


from db import crud


WORK_IN_PROGRESS = 'WIP'
TODAY = datetime.today().strftime('%Y%m%d')
actions = ['GET', 'UPDATE', 'INSERT', 'DELETE']
buttons_actions = [Button.inline(x) for x in actions]

# Use your own values from my.telegram.org
API_ID = config['Telegram']['API_ID']
API_HASH = config['Telegram']['API_HASH']
BOT_TOKEN = config['Telegram']['BOT_TOKEN']
session_name = './sessions/Bot'
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = f"Hi {sender.username}\n" + "CRUD Bot 🤖 ready\n" +\
        "I can perform CRUD operation for you!\n"+\
        "You can add/update/get/delete rows from two tables:\n"+\
        "\"<b>Client</b>\n"+\
        "\"<b>Order</b>\n"
    await client.send_message(
        SENDER, 
        text,
        parse_mode="HTML")
    
@client.on(events.NewMessage(pattern="(?i)/clear"))
async def clear(event):
    await start(event)


@client.on(events.NewMessage(pattern="(?i)/add_client"))
async def insert_client(event):
    sender = await event.get_sender()
    SENDER = sender.id
    txt = event.message.text.split(',')
    row = {'name': txt[0].split(' ')[-1], 'company': txt[1], 'address': txt[2]}
    crud.create_client(**row)
    await client.send_message(SENDER, 'Client added.')

@client.on(events.NewMessage(pattern="(?i)/add_order"))
async def insert_order(event):
    sender = await event.get_sender()
    SENDER = sender.id
    txt = event.message.text.split(',')
    row = {'product_name': txt[0].split(' ')[-1], 'quantity': txt[1], 'clients': txt[2]}
    crud.create_client(**row)
    await client.send_message(SENDER, 'Order added.')


@client.on(events.NewMessage(pattern="(?i)/delete_client"))
async def delete_client(event):
    sender = await event.get_sender()
    SENDER = sender.id
    txt = event.message.text.split(',')
    name = txt[0].split(' ')[-1]
    try:
        company = txt[1]
        crud.delete_client(name, company)
        await client.send_message(SENDER,
                              f'Client deleted.')

    except IndexError:
        await client.send_message(SENDER,
                              f'Wrong request. Company name not present.')


    
@client.on(events.NewMessage(pattern="(?i)/delete_all_clients"))
async def delete_clients(event):
    sender = await event.get_sender()
    SENDER = sender.id
    await client.send_message(SENDER,
                              f'Dangerous operation, are you sure to delete all clients?',
                              buttons=[Button.inline('Yes', b'Yes'), Button.inline('No', b'No')])
    
@client.on(events.CallbackQuery(data=b'Yes'))
async def handler(event):
    crud.delete_all_clients()
    await event.answer('Clients deleted.')

@client.on(events.CallbackQuery(data=b'No'))
async def handler(event):
    await start(event)


        
@client.on(events.NewMessage(pattern="(?i)/get_clients"))
async def get_clients(event):
    sender = await event.get_sender()
    SENDER = sender.id
    clients = crud.get_clients()
    for _client in clients:
        await client.send_message(SENDER,
                              f'Name {_client.name}| Company {_client.company}| Address {_client.address}')
        


    


if __name__ == '__main__':
    client.run_until_disconnected()