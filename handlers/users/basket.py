from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.default.default_keyboards import users_menu_uz, users_menu_ru, location_bttn
from loader import dp, types
from utils.db_api.database_settings import basket_settings, get_user, orders_settings


@dp.message_handler(state="*", text=f"📥 Savat")
async def user_basket_handler(message: types.Message, state: FSMContext):
    user_basket = await basket_settings(work='get', chat_id=message.chat.id)
    if user_basket:
        basket_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        userga = f"🛒 Sizning savatingiz\n\n"
        total = 0
        basket_bttn.insert(KeyboardButton(text=f"🏘 Asosiy menyu"))
        basket_bttn.insert(KeyboardButton(text=f"🛍 Buyurtma berish"))
        for basket in user_basket:
            total += basket['narx']
            userga += f"<b>{basket['product']} \t {int(basket['narx']) // int(basket['miqdor'])}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>\n"
            basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
        userga += f"\n💰 Ja'mi: <b>{total}</b> So'm"
        await message.answer(text=userga, reply_markup=basket_bttn)
        await state.set_state('in_basket')
    else:
        await message.answer(text=f"😕 Kechirasiz sizning savatingiz bo'sh")

@dp.message_handler(state="*", text=f"📥 Корзина")
async def basket_ru_handler(message: types.Message, state: FSMContext):
    user_basket = await basket_settings(work='get', chat_id=message.chat.id)
    if user_basket:
        basket_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        userga = f"🛒 Ваша Корзина\n\n"
        total = 0
        basket_bttn.insert(KeyboardButton(text=f"🏘 Главное меню"))
        basket_bttn.insert(KeyboardButton(text=f"🛍 Разместить заказ"))
        for basket in user_basket:
            total += basket['narx']
            userga += f"<b>{basket['product']} \t {int(basket['narx']) // int(basket['miqdor'])}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>\n"
            basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
        userga += f"\n💰 Общий: <b>{total}</b> Сум"
        await message.answer(text=userga, reply_markup=basket_bttn)
        await state.set_state('in_basket')
    else:
        await message.answer(text=f"😕 Извините, ваша корзина пуста")

@dp.callback_query_handler(state='will_buy', text='basket_ru')
async def basket_uz_handler(call: types.CallbackQuery, state: FSMContext):
    user_basket = await basket_settings(work='get', chat_id=call.message.chat.id)
    if user_basket:
        basket_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        userga = f"🛒 Ваша Корзина\n\n"
        total = 0
        basket_bttn.insert(KeyboardButton(text=f"🏘 Главное меню"))
        basket_bttn.insert(KeyboardButton(text=f"🛍 Разместить заказ"))
        for basket in user_basket:
            total += basket['narx']
            userga += f"<b>{basket['product']} \t {int(basket['narx']) // int(basket['miqdor'])}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>\n"
            basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
        userga += f"\n💰 Общий: <b>{total}</b> Сум"
        await call.message.answer(text=userga, reply_markup=basket_bttn)
        await state.set_state('in_basket')
    else:
        await call.answer(text=f"😕 Извините, ваша корзина пуста", show_alert=True)

@dp.callback_query_handler(state='will_buy', text='basket_uz')
async def basket_uz_handler(call: types.CallbackQuery, state: FSMContext):
    user_basket = await basket_settings(work='get', chat_id=call.message.chat.id)
    if user_basket:
        basket_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        userga = f"🛒 Sizning savatingiz\n\n"
        total = 0
        basket_bttn.insert(KeyboardButton(text=f"🏘 Asosiy menyu"))
        basket_bttn.insert(KeyboardButton(text=f"🛍 Buyurtma berish"))
        for basket in user_basket:
            total += basket['narx']
            userga += f"<b>{basket['product']} \t {int(basket['narx']) // int(basket['miqdor'])}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>\n"
            basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
        userga += f"\n💰 Ja'mi: <b>{total}</b> So'm"
        await call.message.answer(text=userga, reply_markup=basket_bttn)
        await state.set_state('in_basket')
    else:
        await call.answer(text=f"😕 Kechirasiz sizning savatingiz bo'sh", show_alert=True)

@dp.message_handler(state='in_basket')
async def in_basket_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    if message.text[0] == "❌":
        await basket_settings(work='delete', product_name=message.text[2:], chat_id=message.chat.id)
        user_basket = await basket_settings(work='get', chat_id=message.chat.id)
        userga = f"✅ {message.text[2:]} Sizning savatingizdan olib tashlandi!\n"
        userga_ru = f"✅ {message.text[2:]} Удален из корзины!"
        if user_basket:
            basket_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            if user[3] == "uz":
                userga += f"\n🛒 Sizning savatingiz:\n"
                basket_bttn.insert(KeyboardButton(text=f"🏘 Asosiy menyu"))
                basket_bttn.insert(KeyboardButton(text=f"🛍 Buyurtma berish"))
                total = 0
                for basket in user_basket:
                    total += basket['narx']
                    userga += f"\n<b>{basket['product']} \t {basket['narx'] // basket['miqdor']}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>"
                    basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
                userga += f"💰 Ja'mi: {total}"
                await message.answer(text=userga, reply_markup=basket_bttn)
            else:
                userga += f"\n🛒 Ваша Корзина:\n"
                basket_bttn.insert(KeyboardButton(text=f"🏘 Главное меню"))
                basket_bttn.insert(KeyboardButton(text=f"🛍 Разместить заказ"))
                total = 0
                for basket in user_basket:
                    total += basket['narx']
                    userga += f"\n<b>{basket['product']} \t {basket['narx'] // basket['miqdor']}</b> * <b>{basket['miqdor']}</b> = <b>{basket['narx']}</b>"
                    basket_bttn.insert(KeyboardButton(text=f"❌ {basket['product']}"))
                userga += f"💰 Общий: {total}"
                await message.answer(text=userga_ru, reply_markup=basket_bttn)
        else:
            if user[3] == "uz":
                await message.answer(text=userga, reply_markup=users_menu_uz)
            else:
                await message.answer(text=userga_ru, reply_markup=users_menu_ru)
            await state.finish()
    elif message.text[0] == "🛍":
        is_working = await orders_settings(work='is_curer_working')
        status = False
        for is_work in is_working:
            if is_work['is_working'] == True:
                status = True
        if status == True:
            if user[3] == "uz":
                await message.answer(text=f"Quyidagilardan birini tanlang.", reply_markup=await location_bttn(my_locations='Mening manzillarim', send_location='Joylashuv yuborish', cancel='Bekor qilish'))
            else:
                await message.answer(text=f"Quyidagilardan birini tanlang.", reply_markup=await location_bttn(my_locations='Мои адреса', send_location='Отправить местоположение', cancel='Отмена'))
            await state.set_state('waiting_location')
        else:
            if user[3] == "uz":
                await message.answer(text=f"😕 Kechirasiz hozirda ishlayotgan kuryerlar yo'q", reply_markup=users_menu_uz)
            else:
                await message.answer(text=f"😕 К сожалению, на данный момент курьеры не работают.", reply_markup=users_menu_ru)
            await state.finish()