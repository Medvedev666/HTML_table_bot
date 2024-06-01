from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup
)


async def make_buttons(buttons_list):
    keyboard = []
    keyboard_second = []

    for button_text, callback_data in buttons_list:
        if 'http' in callback_data:
            button = InlineKeyboardButton(text=button_text, url=callback_data)
        elif 'Порекомендовать бот' in button_text:
            button = InlineKeyboardButton(text=button_text, switch_inline_query=callback_data)
        else:
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard_second.append(button)
        if callback_data == '#':
            keyboard.append(keyboard_second)
            keyboard_second = []
    keyboard.append(keyboard_second)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def keyboard(button_text):
    keyboard = [[KeyboardButton(button) for button in button_text]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)