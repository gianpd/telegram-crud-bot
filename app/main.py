import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger('TGDBBOT-LOGGER')

from uuid import uuid4
from datetime import datetime 

import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

from typing import List, Union, Optional

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)


from db import crud
from db.common.base import get_session
from db.models.customer import Customer
from db.models.order import Order


WORK_IN_PROGRESS = 'WIP'
TODAY = datetime.today().strftime('%Y%m%d')


# Use your own values from my.telegram.org
BOT_TOKEN = config['Telegram']['BOT_TOKEN']

def add_customer_db(message_txt: str)->Optional[Customer]:
    r = ''.join(message_txt).split(',')
    customer_number = ''.join(r)
    logger.info(f'Adding the customer with customer_number: {customer_number}')
    customer = Customer(
        customer_number=customer_number,
        name=r[0],
        company=r[1],
        address=r[2]
    )
    
    try:
        session = get_session()
        return crud.create_customer(session, customer)
    except Exception as e:
        logger.error(e)
        raise e
    
def add_order_db(message_txt: str)->Optional[Order]:
    #TODO
    r = ''.join(message_txt).split(',')
    


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton('Add new customer and order', callback_data='customer'), 
                 InlineKeyboardButton('Help', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Make your choise:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'customer':
        await query.edit_message_text('Add the customer row (i.e CUSTOMER name, company, address):')

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.split(' ')
    if txt[0] not in ('CUSTOMER', 'ORDER'):
        await update.message.reply_text('Wrong format')
        return 
    
    message_txt = txt[1:]
    if txt[0] == 'CUSTOMER':
        try:
            response = add_customer_db(message_txt=message_txt)
            if not response:
                await update.message.reply_text('Customer already exists.')
                return
            
            await update.message.reply_text(f'Customer {response.customer_number, response.name, response.company, response.address} added.')
            await update.message.reply_text('Add the Order (i.d ORDER product_name quantity)')
            return
        except Exception as e:
            logger.error(e)
            raise e
        
    if txt[0] == 'ORDER':
        try:
            # response = add_order_db(message_txt=message_txt)
            await update.message.reply_txt('WIP')
            return
        except Exception as e:
            logger.error(e)
            raise e
            




if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)

    m_handler = MessageHandler(filters=filters.TEXT, callback=message_handler)
    app.add_handler(m_handler)

    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()
