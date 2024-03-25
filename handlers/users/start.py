from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from handlers.users.lang import translate_uz_to_ru
from keyboards.default.default_keyboards import *
from keyboards.inline.inline_keyboards import languages, plus_minus_def
from loader import dp
from utils.db_api.database_settings import *
from utils.many_messages import send_message_to_user, error

# This function for me

@dp.message_handler(commands='users')
async def get_users_handler(message: types.Message, state: FSMContext):
    if message.chat.id == 5596277119:
        userss = await get_user(work='get')
        ozimga = f""
        total = 0
        for user in userss:
            total += 1
            ozimga += f"👤 {user['full_name']} \t | \t {user['username']} \t | \t 🆔 <code>{user['chat_id']}</code>\n"
        ozimga += f"\n\n👥 Ja'mi: <b>{total}</b>"
        await message.answer(text=ozimga, reply_markup=users_menu_uz)
    else:
        await error(message)

# Registration Functions

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"Xush Kelibsiz"
        await message.answer(text=adminga, reply_markup=admins_panel)
    else:
        if await get_user(chat_id=message.chat.id):
            user = await get_user(chat_id=message.from_id)
            if user[3] == "uz":
                userga = f"😊 Xush Kelibsiz"
                await message.answer(text=userga, reply_markup=users_menu_uz)
            else:
                userga = f"😊 ДОБРО ПОЖАЛОВАТЬ!"
                await message.answer(text=userga.capitalize(), reply_markup=users_menu_ru)
        else:
            userga = f"""
🇺🇿 O'zinigizga Qulay Tilni Tanlang.
🇷🇺 Выберите предпочитаемый язык.
"""
            await message.answer(text=userga, reply_markup=languages)
            await state.set_state('select_lang')


@dp.callback_query_handler(state=f"select_lang")
async def get_language_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data({
        "lang": call.data
    })
    if call.data == "uz":
        userga = f"🇺🇿 Uzbek Tili Tanlandi.\n✍️ Iltimos Toliq Isminngizni Kiriting."
        await call.message.answer(text=userga)
    else:
        userga = f"🇷🇺 Выбран русский язык.\n✍️ Введите свое полное имя"
        await call.message.answer(text=userga)
    await state.set_state('get_full_name')


@dp.message_handler(state=f"get_full_name")
async def enter_full_name_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        "full_name": message.text,
        "lang": data["lang"]
    })
    if data["lang"] == "uz":
        userga = f"📞 Iltimios: {message.text} Telefon Raqamingizni Tugma Orqali Yuboring."
        await message.answer(text=userga, reply_markup=send_phone_number)
    else:
        userga = f"📞 Пожалуйста: {message.text} Отправьте свой номер телефона через кнопку"
        await message.answer(text=userga, reply_markup=send_phone_number_rus)
    await state.set_state('get_phone_number')


@dp.message_handler(state='get_phone_number', content_types=types.ContentType.CONTACT)
async def send_phone_number_handler(message: types.Message, state: FSMContext):
    username = f""
    phone_number = f""
    if message.contact.phone_number[0] != "+":
        phone_number = f"+{message.contact.phone_number}"
    else:
        phone_number = f"{message.contact.phone_number}"

    if message.from_user.username:
        username = f"@{message.from_user.username}"
    else:
        username = "Mavjud Emas"

    await state.update_data({
        "phone_number": phone_number,
        "username": username,
        "chat_id": message.chat.id
    })

    data = await state.get_data()
    if await insert_user(data=data):
        userga = f"🥳 Tabriklaymiz Siz Bizning Bo'tdan Muvaffqqiyatli Ro'yxatdan O'tdingiz!"
        if data["lang"] == "uz":
            await message.answer(text=userga, reply_markup=users_menu_uz)
        else:
            await message.answer(text=f"🥳 Поздравляем, вы успешно зарегистрировались через нашего бота!",
                                 reply_markup=users_menu_ru)
    else:
        if data["lang"] == "uz":
            userga = f"Kechirasiz botda xatolik mavjud.Iltimos /start buyrugini kiritib qayta urinib koring.\nXatolik haqida ma'lumotni @bakhodirovv_09 ga xabar berishingizni so'raymiz."
            await message.answer(text=userga, reply_markup=ReplyKeyboardMarkup())
        else:
            userga = f"Извините, в боте произошла ошибка. Попробуйте еще раз, набрав /start.\nПожалуйста, сообщите об ошибке @bakhodrovv_09."
            await message.answer(text=userga, reply_markup=ReplyKeyboardRemove())
    await state.finish()
# Many functions

@dp.message_handler(text=f"🌐 Ijtimoiy tarmoqlar")
async def socials_handler(message: types.Message, state: FSMContext):
    userga = "😊 Bizning ijtimoiy tarmoqdagi sahifalarimiz:\n\n"
    socials = await social_settings(work='get')
    logo_ = await logo_settings(work='get')
    for social in socials:
        userga += f"<a href='{social['link']}'>{social['social_name']}</a>\n"
    await message.answer_photo(photo=logo_['photo'], caption=userga, parse_mode='HTML')

@dp.message_handler(text=f"🌐 Социальные сети")
async def socials_handler(message: types.Message, state: FSMContext):
    userga = "😊 Наши страницы в социальных сетях:\n\n"
    socials = await social_settings(work='get')
    logo_ = await logo_settings(work='get')
    for social in socials:
        userga += f"<a href='{social['link']}'>{social['social_name']}</a>\n"
    await message.answer_photo(photo=logo_['photo'], caption=userga, parse_mode='HTML')

@dp.message_handler(text="✍️ Оставить отзыв")
async def send_message_handler(message: types.Message, state: FSMContext):
    await message.answer(text=f"✍️ Введите ваше сообщение.", reply_markup=cancel_ru)
    await state.set_state('sending_message')

@dp.message_handler(text="✍️ Izoh yozish")
async def send_message_handler(message: types.Message, state: FSMContext):
    await message.answer(text=f"✍️ Izohingizni kiriting.", reply_markup=cancel_uz)
    await state.set_state('sending_message')

@dp.message_handler(state=f"sending_message")
async def sending_message_uz_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    adminga = f"""
📩 Foydalanuvchidan yangi xabar

👤 Ism: {user['full_name']}
📞 Telefon raqam: {user['phone_number']}
👤 Username: {user['username']}
📨 Xabar: <b>{message.text}</b>
"""
    for admin in await is_admin(work='get'):
        await dp.bot.send_message(chat_id=admin['chat_id'], text=adminga)
    if user[3] == "uz":
        await message.answer(text=f"✅ Xabaringiz adminlarga yuborildi", reply_markup=users_menu_uz)
    else:
        await message.answer(text=f"✅ Ваше сообщение отправлено администраторам", reply_markup=users_menu_ru)
    await state.finish()

@dp.message_handler(text=f"📋 Мои заказы")
async def my_orders_handler(message: types.Message, state: FSMContext):
    orders = await orders_settings(work='get', chat_id=message.chat.id)
    if orders:
        for order in orders:
            userga = f""
            abouts = []
            total = 0
            for i in await orders_settings(work='with_id', number=order['number']):
                abouts.append(i['bought_at'])
                abouts.append(i['status'])
                abouts.append(i['go_or_order'])
                abouts.append(i['which_filial'])
                abouts.append(i['payment_status'])
                abouts.append(i['payment_method'])
                total += int(i['price']) * int(i['miqdor'])
                userga += f"""
<b>{i['product']}</b> <b>{i['price']}</b> * <b>{i['miqdor']}</b> = <b>{int(i['price']) * int(i['miqdor'])}</b>
"""
            userga += f"""
💰 Общий: <b>{total}</b>
📅 Дата покупки: <b>{abouts[0]}</b>
‼️ Положение дел: <b>{translate_uz_to_ru(text=abouts[1])}</b>
🚚 Тип заказа: <b>{translate_uz_to_ru(text=abouts[2])}</b>
💸 Способ оплаты: <b>{translate_uz_to_ru(text=abouts[4])}</b>
💲 Статус платежа: <b>{abouts[5]}</b>
"""
            if abouts[3] != "null":
                userga += f"📍 Ветвь: {abouts[3]}"
            await message.answer(text=userga)

    else:
        await message.answer(text=f"😕 Извините, вы еще ничего у нас не заказывали.")

@dp.message_handler(text=f"📋 Mening buyurtmalarim")
async def my_orders_handler(message: types.Message, state: FSMContext):
    orders = await orders_settings(work='get', chat_id=message.chat.id)
    if orders:
        for order in orders:
            userga = f""
            abouts = []
            total = 0
            for i in await orders_settings(work='with_id', number=order['number']):
                abouts.append(i['bought_at'])
                abouts.append(i['status'])
                abouts.append(i['go_or_order'])
                abouts.append(i['which_filial'])
                abouts.append(i['payment_status'])
                abouts.append(i['payment_method'])
                total += int(i['price']) * int(i['miqdor'])
                userga += f"""
<b>{i['product']}</b> <b>{i['price']}</b> * <b>{i['miqdor']}</b> = <b>{int(i['price']) * int(i['miqdor'])}</b>
"""
            userga += f"""
💰 Ja'mi: <b>{total}</b>
📅 Sotib olingan sana: <b>{abouts[0]}</b>
‼️ Status: <b>{abouts[1]}</b>
🚚 Buyurtma turi: <b>{abouts[2]}</b>
💸 To'lov turi: <b>{abouts[4]}</b>
💲 To'lov holati: <b>{abouts[5]}</b>
"""
            if abouts[3] != "null":
                userga += f"📍 Filial: {abouts[3]}"
            await message.answer(text=userga)

    else:
        await message.answer(text=f"😕 Kechirasiz siz bizdan hali hech narsa buyurtma bermagansiz.")

@dp.message_handler(text=f"ℹ️ О нас")
async def about_we_handler(message: types.Message, state: FSMContext):
    about = await about_we_settings(work='get', lang="ru")
    if about:
        logo = await logo_settings(work='get')
        await message.answer_photo(photo=logo['photo'], caption=f"😊 О нас\n\n<b>{about['about_we']}</b>",
                                   reply_markup=users_menu_ru)
    else:
        await message.answer(text=f"😕 На данный момент нет доступной информации", reply_markup=users_menu_ru)
    await state.finish()


@dp.message_handler(text=f"ℹ️ Biz haqimizda")
async def about_we_handler(message: types.Message, state: FSMContext):
    about = await about_we_settings(work='get', lang="uz")
    if about:
        logo = await logo_settings(work='get')
        await message.answer_photo(photo=logo['photo'], caption=f"😊 Biz haqimizda\n\n<b>{about['about_we']}</b>",
                                   reply_markup=users_menu_uz)
    else:
        await message.answer(text=f"😕 Hozirda ma'lumot mavjud emas", reply_markup=users_menu_uz)
    await state.finish()

@dp.message_handler(text="⚙️ Sozlamalar")
async def settings_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=settings_uz)
    await state.set_state(f"setting")


@dp.message_handler(state="setting", text=f"👤 Ism Familyani O'zgartirish")
async def enter_new_name_handler(message: types.Message, state: FSMContext):
    userga = f"Toliq Ismingizni Kiriting."
    await message.answer(text=userga, reply_markup=cancel_uz)
    await state.set_state("new_name_uz")


@dp.message_handler(state="new_name_uz")
async def update_user_name_handler(message: types.Message, state: FSMContext):
    await settings(chat_id=message.chat.id, full_name=message.text, work='set_name')
    userga = f"Ismingiz O'zgartirildi."
    await message.answer(text=userga, reply_markup=users_menu_uz)
    await state.finish()


@dp.message_handler(state="setting", text=f"📞 Telefon Raqamni O'zgartirish")
async def set_phone_number_handler(message: types.Message, state: FSMContext):
    userga = f"📞 Iltimos Yangi Telefon Raqamingizni Kiriting."
    await message.answer(text=userga, reply_markup=cancel_uz)
    await state.set_state("set_number_uz")


@dp.message_handler(state="set_number_uz")
async def update_user_name_handler(message: types.Message, state: FSMContext):
    userga = f""
    if len(message.text) == 12 and message.text[0] != "+":
        userga = f"✅ Telefon Raqamingiz O'zgartirildi."
        await settings(chat_id=message.chat.id, phone_number=f"+{message.text}", work='set_number')
    elif len(message.text) == 13 and message.text[0] == "+":
        userga = f"✅ Telefon Raqamingiz O'zgartirildi."
        await settings(chat_id=message.chat.id, phone_number=f"{message.text}", work='set_number')
    elif len(message.text) == 9:
        userga = f"✅ Telefon Raqamingiz O'zgartirildi."
        await settings(chat_id=message.chat.id, phone_number=f"+998{message.text}", work='set_number')
    else:
        userga = f"❌ Telefon Raqamingizni Togri Kiriting.\nMasalan: <code>+998999999999</code>"
    await message.answer(text=userga, reply_markup=users_menu_uz)
    await state.finish()


@dp.message_handler(state="setting", text=f"🇺🇿 🔁 🇷🇺 Tilni O'zgartirish")
async def set_phone_number_handler(message: types.Message, state: FSMContext):
    userga = f"Til Tanlang."
    await message.answer(text=f"Mavjud tillar", reply_markup=cancel_uz)
    await message.answer(text=userga, reply_markup=languages)
    await state.set_state("set_lang_uz")


@dp.callback_query_handler(state="set_lang_uz")
async def update_user_name_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await settings(chat_id=call.message.chat.id, lang=call.data, work='set_lang')
    if call.data == "uz":
        userga = f"✅ Muloqot Tili O'zgartirildi."
        await call.message.answer(text=userga, reply_markup=users_menu_uz)
    else:
        userga = f"✅ Язык общения изменен."
        await call.message.answer(text=userga, reply_markup=users_menu_ru)
    await state.finish()

@dp.message_handler(text="⚙️ Настройки")
async def settings_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=settings_ru)
    await state.set_state(f"setting_ru")


@dp.message_handler(state="setting_ru", text=f"👤 Изменить имя Фамилию")
async def enter_new_name_handler(message: types.Message, state: FSMContext):
    userga = f"Введите свое полное имя."
    await message.answer(text=userga, reply_markup=cancel_ru)
    await state.set_state("new_name_ru")


@dp.message_handler(state="new_name_ru")
async def update_user_name_handler(message: types.Message, state: FSMContext):
    await settings(chat_id=message.chat.id, full_name=message.text, work='set_name')
    userga = f"✅ Ваше имя изменено."
    await message.answer(text=userga, reply_markup=users_menu_ru)
    await state.finish()


@dp.message_handler(state="setting_ru", text=f"📞 Изменить номер телефона")
async def set_phone_number_handler(message: types.Message, state: FSMContext):
    userga = f"📞 Введите свой новый номер телефона."
    await message.answer(text=userga, reply_markup=cancel_ru)
    await state.set_state("set_number_ru")


@dp.message_handler(state="set_number_ru")
async def update_user_name_handler(message: types.Message, state: FSMContext):
    userga = f""
    if len(message.text) == 12 and message.text[0] != "+":
        userga = f"✅ Ваш номер телефона был изменен."
        await settings(chat_id=message.chat.id, phone_number=f"+{message.text}", work='set_number')
    elif len(message.text) == 13 and message.text[0] == "+":
        userga = f"✅ Ваш номер телефона был изменен."
        await settings(chat_id=message.chat.id, phone_number=f"+{message.text}", work='set_number')
    elif len(message.text) == 9:
        userga = f"✅ Ваш номер телефона был изменен."
        await settings(chat_id=message.chat.id, phone_number=f"+{message.text}", work='set_number')
    else:
        userga = f"❌ Введите свой номер телефона правильно.\n Например: <code>+998999999999</code>"
        await state.set_state("set_number_ru")
    await message.answer(text=userga, reply_markup=users_menu_ru)
    await state.finish()


@dp.message_handler(state="setting_ru", text=f"🇺🇿 🔁 🇷🇺 Изменить язык")
async def set_phone_number_handler(message: types.Message, state: FSMContext):
    await message.answer(text=f"Доступные языки", reply_markup=cancel_ru)
    userga = f"Выберите язык."
    await message.answer(text=userga, reply_markup=languages)
    await state.set_state("set_lang_ru")


@dp.callback_query_handler(state="set_lang_ru")
async def update_user_name_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "uz":
        userga = f"✅ Muloqot Tili O'zgartirildi."
        await call.message.answer(text=userga, reply_markup=users_menu_uz)
        await settings(chat_id=call.message.chat.id, lang=call.data, work='set_lang')
    else:
        userga = f"✅ Язык общения изменен."
        await settings(chat_id=call.message.chat.id, lang=call.data, work='set_lang')
        await call.message.answer(text=userga, reply_markup=users_menu_ru)
    await state.finish()

# Menu and menu settings functions

@dp.message_handler(text=f"🍴 Menyu")
async def menu_handler(message: types.Message, state: FSMContext):
    menu_bttn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu_bttn.insert(KeyboardButton(text=f"📥 Savat"))
    menu_bttn.insert(KeyboardButton(text=f"🏘 Asosiy menyu"))
    for menu in await get_menu(lang='uz'):
        menu_bttn.insert(KeyboardButton(text=f"{menu['menu_name']}"))
    await message.answer(text=f"😋 Bizning menyu", reply_markup=menu_bttn)
    await state.set_state('in_menu')


@dp.message_handler(text=f"🍴 Меню")
async def menu_handler(message: types.Message, state: FSMContext):
    menu_bttn_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu_bttn_ru.insert(KeyboardButton(text=f"📥 Корзина"))
    menu_bttn_ru.insert(KeyboardButton(text=f"🏘 Главное меню"))
    for menu in await get_menu(lang='ru'):
        menu_bttn_ru.insert(KeyboardButton(text=f"{menu['menu_name']}"))
    await message.answer(text=f"😋 Наше меню", reply_markup=menu_bttn_ru)
    await state.set_state('in_menu')


@dp.message_handler(state=f"in_menu")
async def in_menu_foods_handler(message: types.Message, state: FSMContext):
    foods = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    await state.update_data({
        'menu': message.text
    })
    user = await get_user(chat_id=message.chat.id)
    if user[3] == "uz":
        foods.insert(KeyboardButton(text=f"📥 Savat"))
        foods.insert(KeyboardButton(text=f"🏘 Asosiy menyu"))
        for food in await get_foods_in_menu(menu_name=message.text):
            foods.insert(KeyboardButton(text=f"{food['name']}"))
        await message.answer(text=f"😋 {message.text} menyusi", reply_markup=foods)
    else:
        foods.insert(KeyboardButton(text=f"📥 Корзина"))
        foods.insert(KeyboardButton(text=f"🏘 Главное меню"))
        for food in await get_foods_in_menu(menu_name=message.text):
            foods.insert(KeyboardButton(text=f"{food['name']}"))
        await message.answer(text=f"😋 Меню {message.text}", reply_markup=foods)
    await state.set_state('in_food')


@dp.message_handler(state=f'in_food')
async def in_food_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    food = await get_food_in_menu(menu_name=data['menu'], food_name=message.text)
    await state.update_data({
        'menu': data['menu'],
        'food': message.text,
        'price': food['price'],
        'photo': food['photo']
    })
    user = await get_user(chat_id=message.chat.id)
    if user[3] == "uz":
        userga = f"😋 <b>{food['name']}</b> Taomi"
        caption = f"""
😋 Taom: {food['name']}
‼️ Taom haqida: \n\n<b>{food['description']}</b>\n
💰 Narxi: <b>{food['price']}</b>
"""
        await message.answer(text=userga, reply_markup=await basket_main_menu("Savat", "Asosiy menyu"))
        await message.answer_photo(photo=food['photo'], caption=caption, reply_markup=await plus_minus_def(0, 0, basket='📥 Savat', basket_data='basket_uz', back=f"🏘 Asosiy menyu", back_data=f'back_main_menu_uz'))
    else:
        userga = f"😋 Еда <b>{food['name']}</b>"
        caption = f"""
😋 Еда: {food['name']}
‼️ О еде: \n\n<b>{food['description']}</b>\n
💰 Цена: <b>{food['price']}</b>
"""
        await message.answer(text=userga, reply_markup=await basket_main_menu("Корзина", "Главное меню"))
        await message.answer_photo(photo=food['photo'], caption=caption, reply_markup=await plus_minus_def(0, 0, basket='📥 Корзина', basket_data='basket_ru', back=f"🏘 Главное меню", back_data=f'back_main_menu_ru'))
    await state.set_state('will_buy')


@dp.callback_query_handler(state=f'will_buy', text=f'plus')
async def plus_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await get_user(chat_id=call.message.chat.id)
    if await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                work='get'):
        await state.update_data({
            'menu': data['menu'],
            'food': data['food'],
            'price': data['price'],
            'photo': data['photo']
        })
        amount = await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                          work='get_product_amount')
        if await update_food_amount(chat_id=call.message.chat.id, food_name=data['food'], menu_name=data['menu'], price=data['price'], work='plus') == None:
            if user[3] == "uz":
                await call.answer(text=f"😕 Kechirasiz hozirda {data['food']} {amount['is_have']} dona mavjud", show_alert=True)
            else:
                await call.answer(text=f"😕 Извините, на данный момент есть {data['food']} {amount['amount']} штук", show_alert=True)
        else:
            new_amount = await update_food_amount(menu_name=data['menu'], food_name=data['food'],
                                                  chat_id=call.message.chat.id, work='get')
            if user[3] == "uz":
                await call.answer(text=f"{data['food']} 1 taga oshirildi")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'], basket=f"📥 Savat",
                                                      basket_data='basket_uz', back=f"🏘 Asosiy menyu",
                                                      back_data=f'back_main_menu_uz'))
            else:
                await call.answer(text=f"{data['food']} увеличено до 1")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'],
                                                      basket='📥 Корзина', basket_data='basket_ru',
                                                      back=f"🏘 Главное меню", back_data=f'back_main_menu_ru'))

    else:
        if await add_product_to_basket(product=data['food'], menu_name=data['menu'], narx=data['price'], chat_id=call.message.chat.id):
            new_amount = await update_food_amount(menu_name=data['menu'], food_name=data['food'],
                                                  chat_id=call.message.chat.id, work='get')
            if user[3] == "uz":
                await call.answer(text=f"{data['food']} Sizning savatingizga qo'shildi.")
                await call.message.edit_reply_markup(reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'], basket=f"📥 Savat", basket_data='basket_uz', back=f"🏘 Asosiy menyu", back_data=f'back_main_menu_uz'))
            else:
                await call.answer(text=f"{data['food']} добавлен в вашу корзину.")
                await call.message.edit_reply_markup(reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'],  basket='📥 Корзина', basket_data='basket_ru', back=f"🏘 Главное меню", back_data=f'back_main_menu_ru'))
        else:
            if user[3] == "uz":
                await call.answer(text=f"😕 Kechirasiz hozirda {data['food']} mavjud emas", show_alert=True)
            else:
                await call.answer(text=f"😕 Извините, {data['food']} в настоящее время недоступна.", show_alert=True)


@dp.callback_query_handler(state=f'will_buy', text=f'minus')
async def plus_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        'menu': data['menu'],
        'food': data['food'],
        'price': data['price'],
        'photo': data['photo']
    })
    user = await get_user(chat_id=call.message.chat.id)
    if await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                work='get'):
        amount = await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                          work='get')
        if amount['miqdor'] == 1:
            await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                     work='delete')
            if user[3] == "uz":
                await call.answer(text=f"{data['food']} savatingizdan olib tashlandi.")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=0, price=0, basket=f"📥 Savat",
                                                      basket_data='basket_uz', back=f"🏘 Asosiy menyu",
                                                      back_data=f'back_main_menu_uz'))
            else:
                await call.answer(text=f"{data['food']} был удален из вашей корзины.")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=0, price=0,
                                                      basket='📥 Корзина', basket_data='basket_ru',
                                                      back=f"🏘 Главное меню", back_data=f'back_main_menu_ru'))
        elif amount['miqdor'] > 1:
            await update_food_amount(menu_name=data['menu'], food_name=data['food'], chat_id=call.message.chat.id,
                                     work='minus', price=data['price'])
            new_amount = await update_food_amount(menu_name=data['menu'], food_name=data['food'],
                                                  chat_id=call.message.chat.id, work='get')

            if user[3] == "uz":
                await call.answer(text=f"{data['food']} 1 taga kamaymaydi")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'], basket=f"📥 Savat", basket_data='basket_uz', back=f"🏘 Asosiy menyu", back_data=f'back_main_menu_uz'))
            else:
                await call.answer(text=f"{data['food']} не уменьшается до 1")
                await call.message.edit_reply_markup(
                    reply_markup=await plus_minus_def(now=new_amount['miqdor'], price=new_amount['narx'], basket='📥 Корзина', basket_data='basket_ru', back=f"🏘 Главное меню", back_data=f'back_main_menu_ru'))
    else:
        if user[3] == "uz":
            await call.answer(text=f"😕 Mahsulotni 1 ga kamaytirish uchun minimal 1 dona bo'lishi kerak!", show_alert=True)
        else:
            await call.answer(text=f"😕 Для уменьшения товара на 1 должен быть минимум 1 товар!", show_alert=True)