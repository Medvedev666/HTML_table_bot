from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes, 
    ConversationHandler,
)
from telegram.constants import ParseMode


from .functions import keyboard, make_buttons
from .config import logger
from .list import main_menu

import subprocess

PLATFORM_NAME, RANGE = range(2)

async def make_links(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Введите ID вашей google таблицы\n\n"
                                    "Введите '/cancel' для отмены", 
                                reply_markup=await keyboard(['/cancel']))
    return PLATFORM_NAME


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Вы вышли из формы создания HTML таблицы",
                                reply_markup=ReplyKeyboardRemove())
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Ознакомся с инструкцией и пользуйся 👍",
                                reply_markup=await make_buttons(main_menu))
    return ConversationHandler.END


async def make_range(update, context):

    context.user_data['table_id'] = update.message.text

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Введите диапазон ячеек вашей таблицы, например A1:C4\n"
                                    "Допустимые значения в пределах A:Z\n\n"
                                    "Введите '/cancel' для отмены", 
                                reply_markup=await keyboard(['/cancel']))
    return RANGE



