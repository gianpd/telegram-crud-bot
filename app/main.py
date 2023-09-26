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
from db.models import Customer, Order


WORK_IN_PROGRESS = 'WIP'
TODAY = datetime.today().strftime('%Y%m%d')


# Use your own values from my.telegram.org
BOT_TOKEN = config['Telegram']['BOT_TOKEN']
CUSTOMER_IDS = []

def add_row_db(msg_txt: str, customer_id: Optional[Union[None, int]]=None) -> None:
    """
    Utils for adding a new customer or order to the DB. Both new customers and orders require
    a uid which is generate by joining their field
    """
    r = ''.join(msg_txt).split(',')
    row_uid = ''.join(r)
    logger.info(f'Adding new row with uid: {row_uid}')
    if customer_id:
        # new order: One-to-Many relationship
        order_number = str(customer_id) + row_uid
        order = Order(
            customer_id=customer_id,
            order_number=order_number,
            product_name=r[0],
            quantity=r[1],
        )
        logger.info(f'Trying to add new order: {order.__dict__}')
        try:
            return crud.create_order(order)
        except Exception as e:
            logger.error(e)
            raise e
        
    customer = Customer(
        customer_number=row_uid,
        name=r[0],
        company=r[1],
        address=r[2]
    )
    try:
        return crud.create_customer(customer)
    except Exception as e:
        logger.error(e)
        raise e



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton('Add new customer and order', callback_data='customer'), 
                 InlineKeyboardButton('Help', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Make your choice:', reply_markup=reply_markup)

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
            customer = add_row_db(msg_txt=message_txt)
            customer_id = customer.id
            CUSTOMER_IDS.append(customer_id)
            if not customer:
                await update.message.reply_text('Customer already exists.')
                return
            
            await update.message.reply_text(f'Customer {customer.__dict__} added.')
            await update.message.reply_text('Add the Order (i.d ORDER product_name quantity)')
            return
        except Exception as e:
            logger.error(e)
            raise e
        
    if txt[0] == 'ORDER':
        try:
            # response = add_order_db(message_txt=message_txt)
            if not len(CUSTOMER_IDS):
                await update.message.\
                    reply_text('No customer id provided. Before to add a new order add a customer')
                return
            order = add_row_db(msg_txt=message_txt, customer_id=CUSTOMER_IDS[-1])
            logger.info(f'New order added: {order.__dict__}')
            await update.message.reply_text(f'New order added: {order.__dict__}')
            return
        except Exception as e:
            logger.error(e)
            raise e
    return
            

if __name__ == '__main__':
#   Create the Telegram APP and add its handlers
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)
    m_handler = MessageHandler(filters=filters.TEXT, callback=message_handler)
    app.add_handler(m_handler)
    app.add_handler(CallbackQueryHandler(button))

#   Start the Telegram client
    app.run_polling()