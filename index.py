from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    InlineQueryHandler, 
    CallbackContext, 
    CallbackQueryHandler,
    ConversationHandler
)
from telegram.constants import ParseMode

from config.config import TOKEN, logger, RANGE_LIST
from config.functions import make_buttons, keyboard
from config.list import main_menu
from config.converstation import *

import os



application = ApplicationBuilder().token(TOKEN).build()
switch = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Добро пожаловать, {first_name}\n'
                                'Я помогу тебе быстро перевести твою google таблицу '
                                'в HTML код.\nОзнакомся с инструкцией и пользуйся', 
                                parse_mode=ParseMode.HTML,
                                reply_markup=await make_buttons(main_menu))


async def callback_handler(update: Update, context: CallbackContext):

    callback_data = update.callback_query.data
    call = update.callback_query
    if callback_data == 'main-menu':
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=call.message.message_id,
                                text='Главное меню', reply_markup=await make_buttons(main_menu))
    
    elif callback_data == 'connect':
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text='Напишите в чат Ваш вопрос, наш менеджер ответит вам в '
                                'ближайшее время 😊\n\nДля выхода из режима общения напишите "Выйти"', 
                                reply_markup=await keyboard(['Выйти']))
        


async def start_html(update: Update, context: ContextTypes.DEFAULT_TYPE, sheet_id: str, ranges: str, mes_id: int):

    ranges = ranges.split(":")
    start_index = ranges[0].upper()
    end_index = ranges[1].upper()
    ranges = [f'{start_index}', f'{end_index}']

    from functions_api import get_table_data
    from config.html_generation import generate_html_table
    try:
        result = get_table_data(sheet_id, ranges)

        html_table = generate_html_table(result)

        user_id = update.effective_chat.id

        with open(f"time_files/{user_id}_table.html", "w", encoding="utf-8") as file:
            file.write(html_table)

        with open(f"time_files/{user_id}_table.html", "rb") as file:

            await context.bot.delete_message(chat_id=update.effective_chat.id,
                                            message_id=mes_id)
            await context.bot.send_document(chat_id=update.effective_chat.id,
                                            document=file)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                           text='Для редактирования HTML кода, откройте '
                                'полученный файл с помощью текстового редактора, например "Блокнот"', 
                                reply_markup=await keyboard(['Выйти']))
        os.remove(f"time_files/{user_id}_table.html")
    except Exception as e:
        logger.error(f'Error: {e=}')


async def final_functions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    ranges = update.message.text.split(":")
    start_index = RANGE_LIST.index(ranges[0][0].lower())
    end_index = RANGE_LIST.index(ranges[1][0].lower())

    if end_index < start_index:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f"Введите корректный диапазон. Например А1:С4\n"
                                "Допустимые значения в пределах A:Z",
                            parse_mode=ParseMode.HTML)
        return RANGE

    context.user_data['range'] = update.message.text

    mes = await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   disable_web_page_preview=True,
                                text=f"Данные приняты, пожалуйста подождите...",
                            parse_mode=ParseMode.HTML)
    
    await start_html(update, context, context.user_data['table_id'], 
                    context.user_data['range'], mes.message_id)
    
    return ConversationHandler.END


def main():
    start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(make_links, pattern='^starts$')],
        states={
            PLATFORM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, make_range)],
            RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, final_functions)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    call_back_query = CallbackQueryHandler(callback_handler)

    
    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.add_handler(call_back_query)

    application.run_polling()

if __name__ == '__main__':
    main()