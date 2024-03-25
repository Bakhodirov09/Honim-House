# Admin functions
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.default_keyboards import admin_menu_buttons, cancel_uz, admins_panel, users_menu_uz, end_food, \
    payment_settings, yes_no_def, curers, admins_bttn
from loader import dp
from utils.db_api.database_settings import is_admin, menu_settings, get_foods_in_menu, get_menu, social_settings, \
    logo_settings, payments_settings, cards_settings, curers_settings
from utils.many_messages import error, send_message_to_user, send_error


@dp.message_handler(text=f"⚙️🍴 Menyuni o'zgartirish")
async def change_menu_admin_function_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        await message.answer(text=f"Quyidagilardan birin tanlang.", reply_markup=admin_menu_buttons)
        await state.set_state('changing_menu')
    else:
        await send_message_to_user(message)


@dp.message_handler(state=f'changing_menu')
async def changing_menu_handler(message: types.Message, state: FSMContext):
    menus = await get_menu(lang="uz")
    menus_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    menus_bttn.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    for menyu in menus:
        menus_bttn.insert(KeyboardButton(text=f"{menyu['menu_name']}"))
    if message.text[0] == "🚫":
        await message.answer(text=f"Qaysi menyudagi taom miqdorini kamaytirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('end_meal')
    elif message.text[0] == "✅":
        await message.answer(text=f"Qaysi menyudagi taom miqdorini oshirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('add_amount_meal')
    elif message.text[0] == "➕":
        await message.answer(text=f"Qaysi menyuga taom qoshmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('add_meal')
    elif message.text[0] == "❌":
        await message.answer(text=f"Qaysi menyudagi taomni ochirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('remove_meal')
    elif message.text[0] == "💲":
        await message.answer(text=f"Qaysi menyudagi taom narxini o'zgartirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('change_price')
    elif message.text[0] == "📔":
        await message.answer(text=f"Qaysi menyudagi taom ma'lumotini o'zgartirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('change_desc')
    elif message.text[0] == "✍️":
        await message.answer(text=f"Qaysi menyudagi taom nomini o'zgartirmoqchisiz?", reply_markup=menus_bttn)
        await state.set_state('change_name')
    elif message.text[0] == "🍴":
        await message.answer(text=f"Yangi menyu nomini kiriting.", reply_markup=cancel_uz)
        await state.set_state('new_menu_name')
    else:
        await error(message)
        await state.finish()


@dp.message_handler(state='new_menu_name')
async def new_menu_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu_name': message.text,
    })
    await message.answer(text=f"Yangi menyuning ruscha nomini kiriting.", reply_markup=cancel_uz)
    await state.set_state('new_menu_ru')


@dp.message_handler(state=f"new_menu_ru")
async def new_menu_ru_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu_name_ru': message.text
    })
    await menu_settings(data=await state.get_data(), work='add_new_menu')
    await message.answer(text=f"✅ Yangicha menyu qo'shildi", reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(state=f"end_meal")
async def end_meal_handler(message: types.Message, state: FSMContext):
    foods = await get_foods_in_menu(menu_name=message.text)
    await state.update_data({
        'menu': message.text
    })
    foods_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    foods_bttn.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    for food in foods:
        foods_bttn.insert(KeyboardButton(text=f"{food['name']}"))
    await message.answer(text=f"Qaysi taom?", reply_markup=foods_bttn)
    await state.set_state('which_food_end_meal')


@dp.message_handler(state=f"which_food_end_meal")
async def which_food_end_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'food': message.text
    })
    await message.answer(text=f"Yangi miqdor kiriting.\n\nAgar qolmagan bo'lsa '❌ Taom qolmadi' tugmasini bosing",
                         reply_markup=end_food)
    await state.set_state('get_new_amount')


@dp.message_handler(state='get_new_amount')
async def get_new_amount_handler(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({
            'amount': int(message.text)
        })
    else:
        await state.update_data({
            'amount': 0
        })
    rus_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rus_menu.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    for food in await get_menu(lang='ru'):
        rus_menu.insert(KeyboardButton(text=f"{food['menu_name']}"))
    await message.answer(text=f"Ushbu taom qaysi rus menyuda joylashgan?", reply_markup=rus_menu)
    await state.set_state('get_new_amount_ru')


@dp.message_handler(state='get_new_amount_ru')
async def get_new_amount_ru_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'ru_menu': message.text
    })
    ru_foods = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    ru_foods.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    for food in await get_foods_in_menu(menu_name=message.text):
        ru_foods.insert(KeyboardButton(text=f'{food["name"]}'))
    await message.answer(text=f"Rus menyudagi qaysi taom?", reply_markup=ru_foods)
    await state.set_state('get_food_amount_ru')

@dp.message_handler(state='get_food_amount_ru')
async def get_food_amount_ru_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'ru_food': message.text
    })
    data = await state.get_data()
    await menu_settings(data=data, work='end_meal')
    await message.answer(text=f"{data['food']} miqdori {data['amount']} donaga o'zgardi", reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(state=f"add_amount_meal")
async def end_meal_handler(message: types.Message, state: FSMContext):
    foods = await get_foods_in_menu(menu_name=message.text)
    await state.update_data({
        'menu': message.text
    })
    foods_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    foods_bttn.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    for food in foods:
        foods_bttn.insert(KeyboardButton(text=f"{food['name']}"))
    await message.answer(text=f"Qaysi taom?", reply_markup=foods_bttn)
    await state.set_state('which_food_add_meal')


@dp.message_handler(state=f"which_food_add_meal")
async def which_food_end_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'food': message.text
    })
    await message.answer(text=f"Yangi miqdor kiriting.", reply_markup=cancel_uz)
    await state.set_state('get_new_amount_add')


@dp.message_handler(state='get_new_amount_add')
async def get_new_amount_handler(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({
            'amount': int(message.text)
        })
        data = await state.get_data()
        await menu_settings(data=data, work='add_amount_meal')
        await message.answer(text=f"{data['food']} miqdori {data['amount']} donaga o'zgardi", reply_markup=admins_panel)
        await state.finish()
    else:
        await message.answer(text=f"‼️ Faqat son kiritish mumkin!")
        await state.set_state('get_new_amount_add')


@dp.message_handler(state='add_meal')
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu': message.text
    })
    await message.answer(text=f"Yangi taom nomini kiriting.", reply_markup=cancel_uz)
    await state.set_state('new_meal_name')


@dp.message_handler(state='new_meal_name')
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=f"Yangi taom ruscha nomini yuboring.", reply_markup=cancel_uz)
    await state.set_state('new_meal_name_ru')


@dp.message_handler(state='new_meal_name_ru')
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name_ru': message.text
    })
    await message.answer(text=f"Yangi taom rasmini yuboring.", reply_markup=cancel_uz)
    await state.set_state('new_meal_picture')


@dp.message_handler(state='new_meal_picture', content_types=types.ContentType.PHOTO)
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'photo': message.photo[-1].file_id
    })
    await message.answer(text=f"Yangi taom haqida ma'lumot yuboring.", reply_markup=cancel_uz)
    await state.set_state('new_meal_desc')


@dp.message_handler(state='new_meal_desc')
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'desc': message.text
    })
    await message.answer(text=f"Yangi taom ma'lumotni ruschasini kiriting.", reply_markup=cancel_uz)
    await state.set_state('new_meal_desc_ru')


@dp.message_handler(state='new_meal_desc_ru')
async def add_meal_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'desc_ru': message.text
    })
    await message.answer(text=f"Yangi taom narxini kiriting.", reply_markup=cancel_uz)
    await state.set_state('new_meal_price')


@dp.message_handler(state='new_meal_price')
async def new_meal_price_handler(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({
            'price': int(message.text)
        })
        ru_menu = await get_menu(lang='ru')
        menu_bttn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for ru in ru_menu:
            menu_bttn.insert(KeyboardButton(text=f"{ru['menu_name']}"))
        await message.answer(text=f"Yangi taom qaysi rus menyuda joylashgan?", reply_markup=menu_bttn)
        await state.set_state('ru_menu')
    else:
        await message.answer(text=f"‼️ Narxni faqat sonlarda kiriting!\nMasaln:\n13500\n13000")
        await state.set_state('new_meal_price')


@dp.message_handler(state='ru_menu')
async def ru_menu_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu_ru': message.text
    })
    data = await state.get_data()
    await menu_settings(data=data, work='add_meal')
    await message.answer(text=f"✅ Yangi taom qo'shildi.", reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(text="🌐 Ijtimoiy tarmoq qo'shish")
async def add_social_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        await message.answer(text=f"😊 Yangi ijtimoy tarmoq qaysi dasturda?", reply_markup=cancel_uz)
        await state.set_state('get_new_social_name')
    else:
        await error(message)
        await state.finish()


@dp.message_handler(state='get_new_social_name')
async def get_new_social_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'social_name': message.text
    })
    await message.answer(text=f"🔗 {message.text}dagi sahifaning linkini yuboring.")
    await state.set_state('new_social_link')


@dp.message_handler(state='new_social_link')
async def new_social_link_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'link': message.text
    })
    data = await state.get_data()
    await social_settings(data=data, work='add')
    await message.answer(text=f"✅ Sahifa qo'shildi")
    await state.finish()


@dp.message_handler(text=f"🖼 Logoni almashtirish")
async def change_logo_handler(message: types.Message, state: FSMContext):
    await message.answer(text=f"😊 Yangi logoni yuboring.", reply_markup=cancel_uz)
    await state.set_state('new_logo')


@dp.message_handler(state='new_logo', content_types=types.ContentType.PHOTO)
async def new_logo_handler(message: types.Message, state: FSMContext):
    await logo_settings(photo=message.photo[-1].file_id, work='update')
    await message.answer(text=f"✅ Logo almashtirildi", reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(text=f"💸 To'lov turlari")
async def change_payment_methods_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"😊 Quyidagilardan birini tanlang."
        await message.answer(text=adminga, reply_markup=payment_settings)
        await state.set_state('setting_payment')
    else:
        await error(message)
        await state.finish()


@dp.message_handler(state='setting_payment')
async def payment_method_handler(message: types.Message, state: FSMContext):
    payments = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for payment in await payments_settings(work='get'):
        payments.insert(KeyboardButton(text=f"{payment['payment_name']}"))
    payments.insert(KeyboardButton(text=f"❌ Bekor Qilish"))
    if message.text[0] == "🚫":
        adminga = f"😊 Qaysi tolov turini ochirib qoymoqchisiz?"
        await message.answer(text=adminga, reply_markup=payments)
        await state.set_state('turning_off_payment')
    elif message.text[0] == "➕":
        adminga = f"✍️ Yangi tolov turini nomini kiriting."
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state('new_payment_method_name')
    elif message.text[0] == "🗑":
        adminga = f"😊 Qaysi tolov turini ochirib tashlamoqchisiz?"
        await message.answer(text=adminga, reply_markup=payments)
        await state.set_state('deleting_payment')
    elif message.text[0] == "👍":
        false_payments_bttn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        adminga = f""
        false_payments = await payments_settings(work='false_payments')
        if false_payments:
            for false_pay in await false_payments:
                false_payments_bttn.insert(KeyboardButton(false_pay['payment_name']))
            false_payments_bttn.insert(KeyboardButton(text=f"❌ Bekor Qilish"))
            adminga = f"⚙️ Qaysi tolov holatini o'zgartirmoqchisiz?"
            await message.answer(text=adminga, reply_markup=false_payments_bttn)
            await state.set_state('change_payment_status')
        else:
            adminga = f"😕 Holati o'chirilgan tolov turlari yo'q"
            await message.answer(text=adminga, reply_markup=admins_panel)
            await state.finish()
    else:
        adminga = f"😕 Bunday funksiya topilmadi."
        await message.answer(text=adminga, reply_markup=admins_panel)
        await state.finish()


@dp.message_handler(state='turning_off_payment')
async def turning_off_handler(message: types.Message, state: FSMContext):
    adminga = f""
    try:
        await payments_settings(work='turn_off', payment_name=message.text)
        adminga = f"✅ {message.text} tolov turi holati ochirildi."
    except Exception as e:
        await send_error(e)
        adminga = f"❌ Kechirasiz botda xatolik yuz berdi iltimos qayta urinib ko'ring."
    await state.finish()
    await message.answer(text=adminga, reply_markup=admins_panel)


@dp.message_handler(state='new_payment_method_name')
async def turning_off_handler(message: types.Message, state: FSMContext):
    adminga = f""
    try:
        await payments_settings(work='add', payment_name=message.text)
        adminga = f"🥳 Yangi to'lov turi qoshildi"
    except Exception as e:
        await send_error(e)
        adminga = f"😔 Kechirasiz botda xatolik yuz berdi iltimos qayta urinib ko'ring."
    await message.answer(text=adminga, reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(state='deleting_payment')
async def turning_off_handler(message: types.Message, state: FSMContext):
    adminga = f""
    try:
        await payments_settings(work='delete', payment_name=message.text)
        adminga = f"✅ Ushbu to'lov turi ochirib yuborildi."
    except Exception as e:
        await send_error(e)
        adminga = f"😔 Kechirasiz botda xatolik yuz berdi iltimos qayta urinib ko'ring."
    await message.answer(text=adminga, reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(state='change_payment_status')
async def turning_off_handler(message: types.Message, state: FSMContext):
    adminga = f""
    try:
        await payments_settings(work='update', payment_name=message.text)
        adminga = f"✅ Ushbu to'lov turi holati yondi."
    except Exception as e:
        await send_error(e)
        adminga = f"😔 Kechirasiz botda xatolik yuz berdi iltimos qayta urinib ko'ring."
    await message.answer(text=adminga, reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(text=f"💳 Karta raqamini almashtirish")
async def change_plastic_card_handler(message: types.Message, state: FSMContext):
    await message.answer(text=f"Yangi karta raqamini kiriting", reply_markup=cancel_uz)
    await state.set_state('change_card')


@dp.message_handler(state='change_card')
async def change_card_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'card_number': message.text
    })
    await message.answer(text=f"👤 Karta raqamiga egalik qiluvchi shahs ism familyasini kiriting.")
    await state.set_state('card_owner')


@dp.message_handler(state=f'card_owner')
async def card_owner_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'owner': message.text
    })
    data = await state.get_data()
    try:
        await cards_settings(work='add', data=data)
        await message.answer(text=f"✅ Karta raqam yangilandi", reply_markup=admins_panel)
    except Exception as e:
        await send_error(e)
        await message.answer(text=f"😕 Kechirasiz xatolik yuz berdi iltimos qayta urinib ko'ring!",
                             reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(text="🚚 Kuryerlar")
async def curers_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"Quyidagi bolimdan birini tanlang."
        await message.answer(text=adminga, reply_markup=curers)
        await state.set_state('setting_curer')
    else:
        await send_message_to_user(message)
        await state.finish()


@dp.message_handler(state='setting_curer')
async def setting_curer_handler(message: types.Message, state: FSMContext):
    if message.text[0] == "➕":
        await message.answer(text=f"✍️ Yangi kuryer ismini kiriting.", reply_markup=cancel_uz)
        await state.set_state('get_new_curer_name')
    elif message.text[0] == "🚫":
        await message.answer(
            text=f"✍️ Ochirib yubormoqchi bolgan kuryer chat_id raqamini kiriting yoki ismini kiriting.",
            reply_markup=cancel_uz)
        await state.set_state('get_delete_curer_name')
    elif message.text[0] == "📄":
        adminga = f"Kuryerlar ro'yxati.\n"
        all_curers = await curers_settings(work='get_all_curers')
        for curer in all_curers:
            adminga += f"👤 Ism: {curer['name']} \t Chat_id: {curer['chat_id']}"
        await message.answer(text=adminga)
    elif message.text[0] == "🚚":
        await curers_settings(work='turn_off_status')
        await message.answer(text=f"✅ Kuryerlar holati ochirildi", reply_markup=admins_panel)
        await state.finish()
    elif message.text[0] == "✅":
        await curers_settings(work='turn_on_status')
        await message.answer(text=f"✅ Kuryerlar holati yondi", reply_markup=admins_panel)
        await state.finish()


@dp.message_handler(state="get_new_curer_name")
async def get_new_curer_name_handler(message: types.Message, state: FSMContext):
    adminga = 'Yangi kuryer <b>CHAT ID</b> raqamini kiriting!'
    await message.answer(text=adminga, reply_markup=cancel_uz)
    await state.update_data({
        "name": message.text.capitalize()
    })
    await state.set_state('get_new_curer_id')


@dp.message_handler(state="get_new_curer_id")
async def get_new_curer_name_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "chat_id": int(message.text)
        })
        data = await state.get_data()
        await curers_settings(work='insert', data=data)
        adminga = f"🥳 Tabriklaymiz yangi kuryer qoshildi."
        await message.answer(text=adminga, reply_markup=admins_panel)
        await state.finish()
    except ValueError:
        adminga = f"Kechirasiz siz yangi kuryer <b>CHAT ID</b> raqamini sonlarda kiritmadingiz!"
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state("get_new_curer_id")
    except Exception as e:
        await send_error(e)
        await message.answer(text=f"😕 Kechirasiz bu chat_id raqamdagi foydalnuvchi botdan topilmadi!")
        await state.finish()


@dp.message_handler(state='get_delete_curer_name')
async def get_delete_curer_name_handler(message: types.Message, state: FSMContext):
    adminga = f""
    if message.text.isdigit():
        adminga = f"⚠️⚠️ Haqiqatdan ham ushbu chat id raqamdagi kuryerni ochirib yubormoqchimisiz?"
    else:
        adminga = f"⚠️⚠️ Haqiqatdan ham: {message.text} ismli kuryerni ochirib yubormoqchimisiz?"
    await state.update_data({
        "name": message.text
    })
    await message.answer(text=adminga, reply_markup=yes_no_def)
    await state.set_state('really_del')


@dp.message_handler(state='really_del')
async def get_delete_curer_name_handler(message: types.Message, state: FSMContext):
    adminga = f""
    data = await state.get_data()
    if message.text == "✅ Xa":
        if await curers_settings(work='delete', data=data):
            adminga = f"✅ Kuryer olib tashlandi."
        else:
            adminga = f"😕 Kechirasiz bu chat_id raqamdagi foydalnuvchi botdan topilmadi!"
    else:
        adminga = f"{message.text[0]} Bekor qilindi."
    await state.finish()
    await message.answer(text=adminga, reply_markup=admins_panel)


@dp.message_handler(text="👤 Adminlar")
async def admin_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"Quyidagilardan birini tanlang."
        await message.answer(text=adminga, reply_markup=admins_bttn)
        await state.set_state("setting_admin")
    else:
        await error(message)


@dp.message_handler(state="setting_admin", text="➕👤 Yangi admin qoshish")
async def admin_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"😊 Yangi admin <b>CHAT ID</b> raqamini kiriting."
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state("sending_admin_chat_id")
    else:
        await send_message_to_user(message)


@dp.message_handler(state="sending_admin_chat_id")
async def admin_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "chat_id": int(message.text)
        })
        adminga = f"✍️ Yangi adminning ismini kiriting"
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state("get_admin_name")
    except ValueError:
        adminga = "😕 Kechirasiz yangi admin <b>CHAT ID</b> raqamini faqat butun sonlarda kiritishingiz mumkin!"
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state('sending_admin_chat_id')


@dp.message_handler(state='get_admin_name')
async def got_admin_name_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "name": message.text
        })
        data = await state.get_data()
        await dp.bot.send_message(chat_id=data['chat_id'],
                                  text=f"🥳 Tabriklaymiz: {message.text} siz ushbu botda adminlik huquqiga ega boldingiz!",
                                  reply_markup=admins_panel)
        await is_admin(work='add', data=data)
        await message.answer(text=f"🥳 Tabriklaymiz yangi admin adminlar bolimiga qoshildi!", reply_markup=admins_panel)
        await state.finish()
    except Exception as e:
        adminga = f"😕 Kechirasiz botda xatolik yuz berdi iltimos qayta urunib koring!"
        await send_error(e)
        await message.answer(text=adminga, reply_markup=admins_panel)
        await state.finish()


@dp.message_handler(state='setting_admin', text=f"🚫👤 Admin olib tashlash")
async def remove_admin_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = ""
        all_admins = await is_admin(work='get')
        for admin in all_admins:
            adminga += f"🆔 Chat_id: <code>{admin['chat_id']}</code> 👤 Ism: <b>{admin['name']}</b>\n\n"
        adminga += f"Olib tashlamoqchi bolgan adminingiz <b>CHAT ID</b> raqamini kiriting!"
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state('getting_chatid_dl')
    else:
        await send_message_to_user(message)


@dp.message_handler(state='getting_chatid_dl')
async def got_admin_chat_id_handler(message: types.Message, state: FSMContext):
    try:
        adminga = f"👍 Ushbu admin adminlar orasidan olib tashlandi."
        await dp.bot.send_message(chat_id=int(message.text),
                                  text=f'😕 Kechirasiz siz adminlar orasidan olib tashlandingiz.',
                                  reply_markup=users_menu_uz)
        await is_admin(chat_id=int(message.text), work='delete')
        await message.answer(text=adminga, reply_markup=admins_panel)
        await state.finish()
    except ValueError:
        adminga = f"😕 Kechirasiz admin chat_id raqamini faqat sonlarda kiritish mumkin!"
        await message.answer(text=adminga, reply_markup=cancel_uz)
        await state.set_state('getting_chatid_dl')
    except Exception as e:
        await send_error(e)
        adminga = f"😕 Kechirasiz botda xatolik yuz berdi iltimos qayta urinib koring!"
        await message.answer(text=adminga, reply_markup=admins_panel)
        await state.finish()


@dp.message_handler(state='setting_admin', text=f"📄👤 Adminlar")
async def get_all_admins_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        adminga = f"Ushbu botdagi barcha adminlar ro'yxati.\n\n"
        all_admins = await is_admin(work='get')
        for admin in all_admins:
            adminga += f"🆔 Chat_id: <code>{admin['chat_id']}</code> 👤 Ism: {admin['name']}\n"
        await message.answer(text=adminga, reply_markup=admins_panel)
    else:
        await send_message_to_user(message)
    await state.finish()
