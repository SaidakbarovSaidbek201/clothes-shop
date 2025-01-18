import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMINS
from keyboards import start_keyboards, contact, menu_keyboards, product_keyboards_by_category, product_keyboards_by_id
from database import create_db, user_in_database, add_data_to_users, get_user_id, hozirgi_userni_olish,  get_c_id_by_name, get_product_by_id, add_data_user_product, add_data_to_cart, get_user_product
from state import RegisterState, CategoryState, ProductState, DelCategoryState, DelProductState
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

async def on_startup(dp):
    create_db()
    logging.info("Database initialized successfully.")

@dp.message_handler(commands=['start'])
@dp.message_handler(lambda message: message.text == '🔙 Orqaga')
async def start_command(message: types.Message):
        if user_in_database(message.from_user.id):
            user = hozirgi_userni_olish(message.from_user.id)
            await message.answer(f"👤 Assalomu aleykum, {user['name']}!", reply_markup=start_keyboards)
        else:
            await message.answer("👤 Assalomu aleykum, ro'yhatdan o'tish kerak /register")

@dp.message_handler(commands=['register'])
async def register_command(message: types.Message):
    await RegisterState.name.set()
    await message.answer("Ismingizni kiriting:")

@dp.message_handler(state=RegisterState.name)
async def register_name(message: types.Message, state):
    await state.update_data(name=message.text)
    await RegisterState.next()
    await message.answer("Telefon raqamingizni kiriting:", reply_markup=contact)

@dp.message_handler(state=RegisterState.telefon, content_types=types.ContentTypes.CONTACT)
async def register_phone(message: types.Message, state):
    user_data = await state.get_data()
    add_data_to_users(user_data['name'], message.contact.phone_number, message.from_user.id)
    await state.finish()
    await message.answer("Ro'yhatdan o'tdingiz!", reply_markup=start_keyboards)

@dp.message_handler(lambda message: message.text == 'Kiyimlar')
async def show_menu(message: types.Message):
    await message.answer("Kiyimla:", reply_markup=menu_keyboards())

@dp.callback_query_handler(lambda call: call.data.startswith('add_to_cart'))
async def add_to_cart(call: types.CallbackQuery):
    product_id = call.data.split('_')[-1]
    user = get_user_id(call.from_user.id)
    if user:
        add_data_user_product(user['id'], product_id)
        await call.message.answer("Savatga qo'shildi ✅")

@dp.message_handler(lambda message: message.text == '🛍 Mening zakazlarim')
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    cart_items = get_user_product(user_id)
    if not cart_items:
        await message.answer("Sizning savatingiz bo'sh!")
        return
    else:
        total_price = 0
        text = ""
        for item in cart_items:
            product = get_product_by_id(item['product_id'])
            total_price += product['price']
            text += f"{product['name']} - {product['price']} so'm\n"

        await message.answer(f"{text}\nJami: {total_price} so'm", reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton("✅ Tasdiqlash")], [types.KeyboardButton("❌ Bekor qilish")]],
            resize_keyboard=True
    ))

@dp.message_handler(lambda message: message.text == "✅ Tasdiqlash")
async def confirm_order(message: types.Message):
    await message.answer("Zakazingiz qabul qilindi! ✅")
    user_id = get_user_id(message.from_user.id)
    cart_items = get_user_product(user_id)
    total_price = 0
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        total_price += product['price']
    add_data_to_cart(user_id, cart_items, total_price)
    await bot.send_message(ADMINS[0], f"Yangi zakaz: \nFoydalanuvchi: {message.from_user.full_name}\nMahsulotlar: {cart_items}\nJami: {total_price} so'm")
    

@dp.message_handler(lambda message: message.text == "❌ Bekor qilish")
async def cancel_order(message: types.Message):
    await message.answer("Zakaz bekor qilindi! ❌") 


@dp.message_handler()
async def category_handler(message: types.Message):
    text = message.text
    kategory_id = get_c_id_by_name(text)
    await message.answer(text=f"{text}ni ichidagi mahsulotlar", reply_markup=product_keyboards_by_category(kategory_id))

@dp.callback_query_handler()
async def product_handler(call: types.CallbackQuery):

    if call.data == "back":
        await call.message.answer("Kiyimlar", reply_markup=menu_keyboards())
        return
    
    product_id = call.data
    mahsulot = get_product_by_id(id=product_id)
    c = f"{mahsulot.get('name')} - narxi: {mahsulot.get('price')} so'm" 
    await call.message.answer_photo(photo=mahsulot.get("image"), caption=c, reply_markup=product_keyboards_by_id(product_id))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
