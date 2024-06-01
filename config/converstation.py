from telegram import Update
from telegram.ext import (
    ContextTypes, 
    ConversationHandler,
)
from telegram.constants import ParseMode


from config.functions import keyboard
from config.config import logger

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
                                text="Вы вышли из формы создания бота")
    return ConversationHandler.END


async def make_range(update, context):

    context.user_data['table_id'] = update.message.text

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Введите диапазон ячеек вашей таблицы, например A1:C4\n"
                                    "Допустимые значения в пределах A:Z\n\n"
                                    "Введите '/cancel' для отмены", 
                                reply_markup=await keyboard(['/cancel']))
    return RANGE



