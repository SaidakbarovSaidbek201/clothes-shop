from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from clothes.models import Clothes, Category


start_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboards.add(KeyboardButton('Kiyimlar'))
start_keyboards.add(KeyboardButton('✍️ Ariza qoldirish'), KeyboardButton('⚙️ Sozlamalar'))



contact = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Telefon raqam jonatish', request_contact=True))


def menu_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    categories = Category.objects.all()
    for category in categories:
        keyboard.add(KeyboardButton(category['nomi']))
    return keyboard.add(KeyboardButton('🔙 Orqaga'))


def product_keyboards_by_category(category_id):
    keyboard = InlineKeyboardMarkup()
    products = Clothes.objects.all()
    for product in products:
        if product['category_id'] == category_id:
            keyboard.add(InlineKeyboardButton(product['nomi'], callback_data=product['id']))
    return keyboard


def product_keyboards_by_id(product_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🛒 Savatchaga qo\'shish', callback_data=f'add_to_cart_{product_id}'))
    keyboard.add(InlineKeyboardButton('🔙 Orqaga', callback_data='back'))
    return keyboard