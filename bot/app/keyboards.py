from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

shirt = "t-shirt"

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,                        # делает клавиатуру маленькой
                           input_field_placeholder='Выберите пункт меню...')  # можно написать любое, это строка, где пишут сообщение и этот текст серый
                           
# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Футболки',callback_data='t-shirt')],
#     [InlineKeyboardButton(text='Кросовки',callback_data='sneakers')],
#     [InlineKeyboardButton(text='Кепки',callback_data='cap')]])



# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправьте номер',   # кнопка для номера телефона
#                                                               request_contact= True)]],
#                                             resize_keyboard=True)



async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text = 'На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()      #в одном ряду может быть до 2 кнопок


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text = item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text = 'На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()      #в одном ряду может быть до 2 кнопок

