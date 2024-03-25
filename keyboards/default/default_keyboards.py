from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"❌ Bekor qilish")
        ]
    ], resize_keyboard=True
)

cancel_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"❌ Отмена")
        ]
    ], resize_keyboard=True
)

send_phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon Raqamni Yuborish", request_contact=True)
        ]
    ], resize_keyboard=True
)

send_phone_number_rus = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Отправить номер телефона", request_contact=True)
        ]
    ], resize_keyboard=True
)

admins_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"⚙️🍴 Menyuni o'zgartirish")
        ],
        [
            KeyboardButton(text=f'👤 Adminlar'),
            KeyboardButton(text=f"🆔 Buyurtmalar")
        ],
        [
            KeyboardButton(text=f"🌐 Ijtimoiy tarmoq qo'shish"),
            KeyboardButton(text=f'🍴 Menyu')
        ],
        [
            KeyboardButton(text="💸 To'lov turlari"),
            KeyboardButton(text="🚚 Kuryerlar"),
        ],
        [
            KeyboardButton(text=f"💳 Karta raqamini almashtirish"),
            KeyboardButton(text=f"🖼 Logoni almashtirish")
        ]
    ], resize_keyboard=True
)

users_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍴 Меню")
        ],
        [
            KeyboardButton(text="📋 Мои заказы"),
            KeyboardButton(text="✍️ Оставить отзыв")
        ],
        [
            KeyboardButton(text="ℹ️ О нас"),
            KeyboardButton(text="🌐 Социальные сети")
        ],
        [
            KeyboardButton(text="⚙️ Настройки")
        ]
    ], resize_keyboard=True
)

yes_no_def = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Xa'),
            KeyboardButton(text="❌ Yo'q")
        ]
    ], resize_keyboard=True
)

yes_no_def_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Да'),
            KeyboardButton(text='❌ Нет')
        ]
    ], resize_keyboard=True
)

curers = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"➕🚚 Yangi kuryer qoshish"),
            KeyboardButton(text=f"🚫🚚 Kuryer olib tashlash")
        ],
        [
            KeyboardButton(text=f"🚚 Kuryerlarni ochirish"),
            KeyboardButton(text=f"✅🚚 Kuryerlarni yoqish"),
        ],
        [
            KeyboardButton(text=f"📄🚚 Kuryerlar"),
            KeyboardButton(text=f"🏘 Asosiy menyu")
        ]
    ], resize_keyboard=True
)

admins_bttn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'➕👤 Yangi admin qoshish'),
            KeyboardButton(text=f'🚫👤 Admin olib tashlash')
        ],
        [
            KeyboardButton(text=f'📄👤 Adminlar'),
            KeyboardButton(text="🏘 Asosiy menyu")
        ]
    ], resize_keyboard=True
)

users_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍴 Menyu")
        ],
        [
            KeyboardButton(text="📋 Mening buyurtmalarim"),
            KeyboardButton(text="✍️ Izoh yozish")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="🌐 Ijtimoiy tarmoqlar")
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    ], resize_keyboard=True
)

admin_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"🚫🍴 Taom miqdor ayirish")
        ],
        [
            KeyboardButton(text="✅🍴 Taom miqdor qoshish")
        ],
        [
            KeyboardButton(text=f"➕ Taom qoshish"),
            KeyboardButton(text=f"🍴➕ Yangicha menyu qoshish"),
        ],
        [
            KeyboardButton(text=f"❌ Taom ochirish"),
            KeyboardButton(text=f"💲🔧 Narx o'zgartirish"),
        ],
        [
            KeyboardButton(text=f"📔🔧 Ma'lumot o'zgartirish"),
            KeyboardButton(text=f"✍️🔧 Taom nomini o'zgartirish"),
        ],
        [
            KeyboardButton(text=f"❌ Bekor qilish")
        ]
    ], resize_keyboard=True
)

settings_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"👤 Ism Familyani O'zgartirish"),
            KeyboardButton(text=f"📞 Telefon Raqamni O'zgartirish"),
        ],
        [
            KeyboardButton(text=f"🇺🇿 🔁 🇷🇺 Tilni O'zgartirish"),
            KeyboardButton(text=f"🏘 Asosiy menyu")
        ]
    ], resize_keyboard=True
)

settings_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"👤 Изменить имя Фамилию"),
            KeyboardButton(text=f"📞 Изменить номер телефона"),
        ],
        [
            KeyboardButton(text=f"🇺🇿 🔁 🇷🇺 Изменить язык"),
            KeyboardButton(text=f"🏘 Главное меню")
        ]
    ], resize_keyboard=True
)
async def basket_main_menu(basket, main_menu):
    basket_and_main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"🏘 {main_menu}"),
                KeyboardButton(text=f"📥 {basket}")
            ]
        ], resize_keyboard=True
    )
    return basket_and_main_menu

end_food = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"❌ Taom qolmadi")
        ]
    ], resize_keyboard=True
)

async def location_bttn(my_locations, send_location, cancel):
    location = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"🗺 {my_locations}")
            ],
            [
                KeyboardButton(text=f"📍 {send_location}", request_location=True),
                KeyboardButton(text=f"❌ {cancel}")
            ]
        ], resize_keyboard=True
    )
    return location

payment_settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"🚫 To'lov holatini o'chirish"),
            KeyboardButton(text=f"🗑 To'lov usulini olib tashlash")
        ],
        [
            KeyboardButton(text=f"➕ Yangi tolov usulini qoshish"),
            KeyboardButton(text=f"👍 Tolov holatini yoqish")
        ],
        [
            KeyboardButton(text=f"🏘 Asosiy menyu")
        ]
    ], resize_keyboard=True
)
