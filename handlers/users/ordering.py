import random

from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.lang import translate_uz_to_ru
from handlers.users.location import get_location_name, get_location_name_ru
from keyboards.default.default_keyboards import users_menu_uz, users_menu_ru, cancel_uz, cancel_ru, yes_no_def, \
    yes_no_def_ru, location_bttn
from loader import dp, types
from utils.db_api.database_settings import get_user, location_settings, payments_settings, curers_settings, \
    basket_settings, cards_settings, is_admin, orders_settings


@dp.message_handler(state='waiting_location')
async def waiting_location_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    user_locations = await location_settings(work='get_locations', chat_id=message.chat.id)
    if user_locations:
        user_locations_bttn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for location in user_locations:
            user_locations_bttn.insert(KeyboardButton(text=f"{location['location_name']}"))
        if user[3] == "uz":
            user_locations_bttn.insert(KeyboardButton(text=f"❌ Bekor qilish"))
            await message.answer(text=f"Sizning joylashuvlaringiz", reply_markup=user_locations_bttn)
        else:
            user_locations_bttn.insert(KeyboardButton(text=f"❌ Отмена"))
            await message.answer(text=f"Ваши местоположения", reply_markup=user_locations_bttn)
        await state.set_state('select_location')
    else:
        if user[3] == "uz":
            await message.answer(text=f"😕 Kechirasiz bizning botda sizning manzillaringiz mavjud emas!")
        else:
            await message.answer(text=f"😕 К сожалению, ваши адреса недоступны в нашем боте!")
        await state.set_state('waiting_location')


@dp.message_handler(state='waiting_location', content_types=types.ContentType.LOCATION)
async def select_location_handler(message: types.Message, state: FSMContext):
    loc = get_location_name(latitude=message.location.latitude, longitude=message.location.longitude)
    location = f"{loc[-1]} {loc[-3]} {loc[-5]} {loc[-4]} {loc[0]}"
    user = await get_user(chat_id=message.chat.id)
    if user[3] == "uz":
        await message.answer(
            text=f"‼️ Siz yuborgan manzil: <b>{location}</b>\nUshbu manzilni tasdiqlaysizmi?",
            reply_markup=yes_no_def)
    else:
        await message.answer(
            text=f"‼️ Адрес, который вы отправили: <b>{location}</b> подтвердить этот адрес?",
            reply_markup=yes_no_def_ru)
    await state.update_data({
        'location_name': location,
        "longitude": message.location.longitude,
        "latitude": message.location.latitude,
        "chat_id": message.chat.id,
    })
    await state.set_state('accept')

@dp.message_handler(state=f"accept")
async def get_location_handler(message: types.Message, state: FSMContext):
    lang = await get_user(chat_id=message.chat.id)
    data = await state.get_data()
    if message.text[0] == "✅":
        await state.update_data({
            "location_name": data['location_name'],
            "longitude": data['longitude'],
            "latitude": data['latitude'],
            "chat_id": data['chat_id'],
        })
        await location_settings(work='add', data=data, location=translate_uz_to_ru(text=data['location_name']))
        payments_bttn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for payment in await payments_settings(work='get'):
            if payment['payment_name'] == "Naqd" or payment['payment_name'] == "Наличные":
                payments_bttn.insert(KeyboardButton(text=f"💸 {payment['payment_name']}"))
            else:
                payments_bttn.insert(KeyboardButton(text=f"💴 {payment['payment_name']}"))

        if lang[3] == "uz":
            payments_bttn.insert(KeyboardButton(text=f"❌ Bekor qilish"))
            userga = f"💸 Tolov turini tanlang."
        else:
            payments_bttn.insert(KeyboardButton(text=f"❌ Отмена"))
            userga = f"💸 Выберите тип оплаты."
        await message.answer(text=userga, reply_markup=payments_bttn)
        await state.set_state('select_payment')
    else:
        if lang[3] == "uz":
            userga = f"‼️ Aniq manzilni yuborng."
            await message.answer(text=userga, reply_markup=await location_bttn(my_locations='Mening manzillarim', send_location='Joylashuv yuborish', cancel='Bekor qilish'))
        else:
            userga = f"‼️ Пожалуйста, пришлите точный адрес."
            await message.answer(text=userga, reply_markup=await location_bttn(my_locations='Мои адреса', send_location='Отправить местоположение', cancel='Отмена'))
        await state.set_state('select_payment')


@dp.message_handler(state='select_location')
async def select_location_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    location = await location_settings(work='get', chat_id=message.chat.id, location=message.text)
    if location:
        await state.update_data({
            'location_name': message.text,
            'latitude': location['latitude'],
            'longitude': location['longitude']
        })
        payments = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for payment in await payments_settings(work='get'):
            if payment['payment_name'] != "Naqd":
                payments.insert(KeyboardButton(text=f"💴 {payment['payment_name']}"))
            else:
                payments.insert(KeyboardButton(text=f"💸 {payment['payment_name']}"))
        payments.insert(KeyboardButton(text=f"❌ Bekor qilish"))
        if user[3] == "uz":
            await message.answer(text=f"💸 To'lov turini tanlang.", reply_markup=payments)
        else:
            await message.answer(text=f"💸 Выберите тип оплаты.", reply_markup=payments)
        await state.set_state('select_payment')
    else:
        if user[3] == "uz":
            await message.answer(text=f"😕 Kechirasiz siz noto'g'ri joylashuv kiritdingiz!")
        else:
            await message.answer(text=f"😕 Извините, вы ввели неверный адрес!")
        await state.set_state('select_location')


@dp.message_handler(state=f"select_payment")
async def select_payment_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    if message.text[0] == "💸":
        await state.update_data({
            'payment_method': message.text[2:]
        })
        data = await state.get_data()
        number = random.randint(1000000, 10000000)
        language = ""
        if user[3] == "uz":
            language = f"🇺🇿 Uzbek tili"
        else:
            language = f"🇷🇺 Rus tili"
        curerga = f"""
👤 Toliq Ism: {user[1]}
👤 Username: {user[2]}
🌐 Til: {language}
📞 Telefon raqam: {user[4]}
🆔 Buyurtma raqami: {number}
🛍 Mahsulotlar:\n
"""
        user_basket = await basket_settings(work='get', chat_id=message.chat.id)
        print(data)
        total = 0
        for basket in user_basket:
            await orders_settings(work='add', chat_id=message.chat.id, number=number, product=basket['product'],
                                  miqdor=basket['miqdor'], price=basket['narx'] // basket['miqdor'],
                                  bought_at=message.date, payment_method=data['payment_method'], go_or_order='Dostavka',
                                  which_filial='null', status='Yetkazilmoqda', payment_status="To'lanmagan")

            total += basket['narx']
            curerga += f"\n<b>{basket['product']} \t {basket['narx'] // basket['miqdor']}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>"
        curerga += f"\n💰 Ja'mi: {total}\n"
        curerga += f"📍 Joylashuv: {data['location_name']}\n"
        curerga += f"💸 To'lov turi: {message.text[2:]}"
        not_working_curer = await curers_settings(work='get_not_working')
        for admin in await is_admin(work='get'):
            await dp.bot.send_message(chat_id=admin['chat_id'], text=curerga)
        curergaa = InlineKeyboardMarkup(row_width=1)
        curergaa.insert(InlineKeyboardButton(text=f"✅ Yetkazildi", callback_data=f'ordered_{message.chat.id}_{number}'))
        await basket_settings(work='delete_basket', chat_id=message.chat.id)
        if not_working_curer:
            await dp.bot.send_location(chat_id=not_working_curer['chat_id'], latitude=data['latitude'],
                                       longitude=data['longitude'])
            await dp.bot.send_message(chat_id=not_working_curer['chat_id'], text=curerga, reply_markup=curergaa)
            if user[3] == "uz":
                await message.answer(text=f"✅ Buyurtmangiz qabul qilindi\n\n🆔 Buyurtma raqamingiz: {number}",
                                     reply_markup=users_menu_uz)
            else:
                await message.answer(text=f"✅ Ваш заказ принят\n\n🆔 Ваш номер заказа: {number}",
                                     reply_markup=users_menu_uz)

        else:
            all_curers = await curers_settings(work='get_all_curers')
            curers = []
            for curer in all_curers:
                curers.append(curer['chat_id'])
            random_curer = random.choice(curers)
            await dp.bot.send_location(chat_id=random_curer, latitude=data['latitude'], longitude=data['longitude'])
            await dp.bot.send_message(chat_id=random_curer, text=curerga, reply_markup=curergaa)
            if user[3] == "uz":
                await message.answer(
                    text=f"✅😔 Buyurtmangiz qabul qilindi, ammo bo'sh kuryer topilmaganligini sabab buyurtmangiz ozgina kechikishi mumkin.Noqulayliklar uchun uzr so'raymiz.\n\n🆔 Buyurtma raqamingiz: {number}",
                    reply_markup=users_menu_uz)
            else:
                await message.answer(
                    text=f"✅😔Ваш заказ получен, но безработный курьер не найден, поэтому ваш заказ может немного задержаться. Приносим извинения за неудобства.\n\n🆔 Номер вашего заказа: {number}",
                    reply_markup=users_menu_ru)
        await state.finish()
    else:
        await state.update_data({
            'payment_method': message.text[2:]
        })
        card = await cards_settings(work='get')
        total = 0
        for basket in await basket_settings(work='get', chat_id=message.chat.id):
            total += basket['narx']
        if user[3] == "uz":
            await message.answer(
                text=f"💳 Plastik karta: <b>{card['card_number']}</b>\n👤 <b>{card['owner']}</b>\n\nUshbu plastik kartaga: {total} miqdorida pul o'tkazing va chekni rasmga olib yuboring.",
                reply_markup=cancel_uz)
        else:
            await message.answer(
                text=f"💳 Пластиковая карта: <b>{card['card_number']}</b>\n👤 <b>{card['owner']}</b>\n\nНа эту пластиковую карту: {total} денег перевод и отправить чек",
                reply_markup=cancel_ru)
        await state.set_state('send_photo')


@dp.message_handler(state=f"send_photo", content_types=types.ContentType.PHOTO)
async def send_check_payment_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    data = await state.get_data()
    number = random.randint(1000000, 10000000)
    language = ""
    if user[3] == "uz":
        language = f"🇺🇿 Uzbek tili"
    else:
        language = f"🇷🇺 Rus tili"
    curerga = f"""
👤 Toliq Ism: {user[1]}
👤 Username: {user[2]}
🌐 Til: {language}
📞 Telefon raqam: {user[4]}
🆔 Buyurtma raqami: {number}
🛍 Mahsulotlar:\n
"""
    user_basket = await basket_settings(work='get', chat_id=message.chat.id)
    total = 0
    for basket in user_basket:
        await orders_settings(work='add', chat_id=message.chat.id, number=number, payment_status="To'langan", product=basket['product'], miqdor=basket['miqdor'], price=basket['narx'] // basket['miqdor'], bought_at=message.date, payment_method=data['payment_method'], go_or_order='Dostavka', which_filial='null', status='Yetkazilmoqda')
        total += basket['narx']
        curerga += f"<b>{basket['product']} \t {basket['narx'] // basket['miqdor']}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>\n"
    curerga += f"\n💰 Ja'mi: {total}\n"
    curerga += f"📍 Joylashuv: {data['location_name']}\n"
    curerga += f"💸 To'lov turi: {data['payment_method']}"
    not_working_curer = await curers_settings(work='get_not_working')
    for admin in await is_admin(work='get'):
        await dp.bot.send_photo(photo=message.photo[-1].file_id, chat_id=admin['chat_id'], caption=curerga)
    await basket_settings(work='delete_basket', chat_id=message.chat.id)
    curergaa = InlineKeyboardMarkup(row_width=1)
    curergaa.insert(InlineKeyboardButton(text=f"✅ Yetkazildi", callback_data=f'ordered_{message.chat.id}_{number}'))
    if not_working_curer:
        await dp.bot.send_location(chat_id=not_working_curer['chat_id'], latitude=data['latitude'],
                                   longitude=data['longitude'])
        await dp.bot.send_photo(photo=message.photo[-1].file_id, chat_id=not_working_curer['chat_id'], caption=curerga, reply_markup=curergaa)
        await curers_settings(work='update', chat_id=not_working_curer['chat_id'])
        if user[3] == "uz":
            await message.answer(text=f"✅ Buyurtmangiz qabul qilindi\n\n🆔 Buyurtma raqamingiz: {number}",
                                 reply_markup=users_menu_uz)
        else:
            await message.answer(text=f"✅ Ваш заказ принят\n\n🆔 Ваш номер заказа: {number}", reply_markup=users_menu_uz)

    else:
        all_curers = await curers_settings(work='get_all_curers')
        curers = []
        for curer in all_curers:
            curers.append(curer['chat_id'])
        random_curer = random.choice(curers)
        await dp.bot.send_location(chat_id=random_curer, latitude=data['latitude'], longitude=data['longitude'])
        await dp.bot.send_photo(chat_id=random_curer, photo=message.photo[-1].file_id, caption=curerga, reply_markup=curergaa)
        await curers_settings(work='update', chat_id=random_curer)
        if user[3] == "uz":
            await message.answer(
                text=f"✅😔 Buyurtmangiz qabul qilindi, ammo bo'sh kuryer topilmaganligini sabab buyurtmangiz ozgina kechikishi mumkin.Noqulayliklar uchun uzr so'raymiz.\n\n🆔 Buyurtma raqamingiz: {number}",
                reply_markup=users_menu_uz)
        else:
            await message.answer(
                text=f"✅😔Ваш заказ получен, но безработный курьер не найден, поэтому ваш заказ может немного задержаться. Приносим извинения за неудобства.\n\n🆔 Номер вашего заказа: {number}",
                reply_markup=users_menu_ru)
    await state.finish()
