from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes, 
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler
)

BOT_TOKEN = "6453528596:AAEwi1sneOrd0TUwTdE5vCnSowI4JJ6fuUc"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [[InlineKeyboardButton('Customer', callback_data='customer'), InlineKeyboardButton('Order', callback_data='order')], 
                [InlineKeyboardButton('Help', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'customer':
        print('CUSTOMER')
    await query.edit_message_text(f'Selected option: {query.data}')



application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler('start', start_handler))
application.add_handler(CallbackQueryHandler(button))
application.run_polling()