from main.database_set import database
from main.models import *


async def get_user(chat_id=None, work=None):
    if chat_id != None:
        return await database.fetch_one(query=users.select().where(users.c.chat_id == chat_id))
    elif work == 'get':
        return await database.fetch_all(query=users.select())


async def is_admin(chat_id=None, work=None, data=None):
    if work == None:
        return await database.fetch_one(query=admins.select().where(admins.c.chat_id == chat_id))
    elif work == "get":
        return await database.fetch_all(query=admins.select())
    elif work == 'add':
        return await database.execute(query=admins.insert().values(
            name=data['name'],
            chat_id=data['chat_id']
        ))
    elif work == 'delete':
        return await database.execute(query=admins.delete().where(
            admins.c.chat_id==chat_id
        ))


async def insert_user(data: dict):
    return await database.execute(query=users.insert().values(
        full_name=data["full_name"],
        username=data["username"],
        lang=data["lang"],
        phone_number=data["phone_number"],
        chat_id=data["chat_id"],
    ))


async def get_menu(lang):
    return await database.fetch_all(query=menu.select().where(menu.c.lang == lang))


async def get_foods_in_menu(menu_name):
    return await database.fetch_all(query=foods_menu.select().where(foods_menu.c.menu == menu_name))


async def get_food_in_menu(food_name, menu_name):
    return await database.fetch_one(
        query=foods_menu.select().where(foods_menu.c.name == food_name, foods_menu.c.menu == menu_name))


async def update_food_amount(menu_name=None, food_name=None, chat_id=None, price=None, work=None):
    if work == 'plus':
        old_amount = await database.fetch_one(query=basket.select().where(
            basket.c.chat_id == chat_id,
            basket.c.product == food_name,
            basket.c.menu_name == menu_name
        ))
        amount = await database.fetch_one(
            query=foods_menu.select().where(foods_menu.c.menu == menu_name, foods_menu.c.name == food_name))
        is_true = int(amount['is_have']) > int(old_amount['miqdor'])
        if is_true == True:
            await database.execute(query=basket.update().values(
                miqdor=old_amount['miqdor'] + 1,
                narx=old_amount['narx'] + price
            ).where(basket.c.chat_id == chat_id, basket.c.product == food_name, basket.c.menu_name == menu_name))
            return True
        else:
            return None
    elif work == 'minus':
        old_amount = await database.fetch_one(query=basket.select().where(
            basket.c.chat_id == chat_id,
            basket.c.product == food_name,
            basket.c.menu_name == menu_name
        ))
        return await database.execute(query=basket.update().values(
            miqdor=old_amount['miqdor'] - 1,
            narx=old_amount['narx'] - price
        ))
    elif work == 'delete':
        return await database.execute(query=basket.delete().where(
            basket.c.chat_id == chat_id,
            basket.c.product == food_name,
            basket.c.menu_name == menu_name
        ))
    elif work == 'get':
        return await database.fetch_one(query=basket.select().where(
            basket.c.chat_id == chat_id,
            basket.c.product == food_name,
            basket.c.menu_name == menu_name
        ))
    elif work == 'get_product_amount':
        return await database.fetch_one(query=foods_menu.select().where(
            foods_menu.c.menu == menu_name,
            foods_menu.c.name == food_name,
        ))


async def menu_settings(data: dict, work):
    if work == 'end_meal':
        await database.execute(query=foods_menu.update().values(
            is_have=data['amount']
        ).where(foods_menu.c.name == data['food'], foods_menu.c.menu == data['menu']))
        await database.execute(query=foods_menu.update().values(
            is_have=data['amount']
        ).where(foods_menu.c.name == data['ru_food'], foods_menu.c.menu == data['ru_menu']))
    elif work == 'add_amount_meal':
        food = await database.fetch_one(query=foods_menu.select().where(
            foods_menu.c.name == data['food'],
            foods_menu.c.menu == data['menu']
        ).with_only_columns(foods_menu.c.photo))
        return await database.execute(query=foods_menu.update().values(
            is_have=data['amount']
        ).where(foods_menu.c.photo == food['photo']))
    elif work == 'add_meal':
        await database.execute(query=foods_menu.insert().values(
            menu=data['menu'],
            name=data['name'],
            description=data['desc'],
            price=data['price'],
            is_have=0,
            photo=data['photo'],
            lang='uz'
        ))
        await database.execute(query=foods_menu.insert().values(
            menu=data['menu_ru'],
            name=data['name_ru'],
            description=data['desc_ru'],
            price=data['price'],
            is_have=0,
            photo=data['photo'],
            lang='ru'
        ))
    elif work == 'add_new_menu':
        await database.execute(query=menu.insert().values(
            menu_name=data['menu_name'],
            lang="uz"
        ))
        await database.execute(query=menu.insert().values(
            menu_name=data['menu_name_ru'],
            lang="ru"
        ))


async def social_settings(data=None, work=None):
    if work == "add":
        return await database.execute(socials.insert().values(
            social_name=data['social_name'],
            link=data['link']
        ))
    elif work == 'get':
        return await database.fetch_all(query=socials.select())


async def about_we_settings(work=None, new_about=None, lang=None, new_about_ru=None):
    if work == 'update':
        if await database.fetch_one(query=about_we.select()):
            await database.execute(query=about_we.update().values(
                about_we=new_about
            ).where(about_we.c.lang == "uz"))
            await database.execute(query=about_we.update().values(
                about_we=new_about_ru
            ).where(about_we.c.lang == "ru"))
        else:
            await database.execute(query=about_we.insert().values(
                about_we=new_about
            ).where(about_we.c.lang == "uz"))
            await database.execute(query=about_we.insert().values(
                about_we=new_about_ru
            ).where(about_we.c.lang == "ru"))
    elif work == "get":
        return await database.fetch_one(query=about_we.select().where(about_we.c.lang == lang))


async def orders_settings(work=None, chat_id=None, number=None, product=None, miqdor=None, price=None, bought_at=None,
                          payment_method=None, go_or_order=None, which_filial=None,
                          status=None, payment_status=None, menu=None, ru_menu=None, ru_product=None):
    if work == "get":
        return await database.fetch_all(query=history_buys.select().where(history_buys.c.chat_id == chat_id))
    elif work == 'with_id':
        return await database.fetch_all(query=history_buys.select().where(history_buys.c.number == number))
    elif work == "is_curer_working":
        return await database.fetch_all(query=curers.select().where(curers.c.is_working == True))
    elif work == "add":
        await database.execute(query=history_buys.insert().values(
            number=number,
            product=product,
            miqdor=miqdor,
            price=price,
            bought_at=bought_at,
            payment_method=payment_method,
            go_or_order=go_or_order,
            which_filial=which_filial,
            chat_id=chat_id,
            payment_status=payment_status,
            status=status,
        ))
    elif work == 'update':
        await database.execute(query=history_buys.update().values(
            status='Haridorga topshirilgan'
        ).where(history_buys.c.number == number))
    elif work == 'minus_amount':
        amount = await database.fetch_one(query=foods_menu.select().where(
            foods_menu.c.menu == menu,
            foods_menu.c.name == product
        ))
        await database.execute(query=foods_menu.update().values(
            is_have=amount['is_have'] - miqdor
        ).where(foods_menu.c.menu == menu, foods_menu.c.name == product, foods_menu.c.menu == ru_menu,
                foods_menu.c.name == ru_product))


async def cards_settings(work=None, data=None):
    if work == "get":
        return await database.fetch_one(query=card_model.select())
    elif work == "add":
        if await database.fetch_one(query=card_model.select()):
            return await database.execute(query=card_model.update().values(
                card_number=data['card_number'],
                owner=data['owner']
            ))
        else:
            return await database.execute(query=card_model.insert().values(
                card_number=data['card_number'],
                owner=data['owner']
            ))


async def location_settings(work=None, data=None, chat_id=None, location=None):
    if work == 'get_locations':
        return await database.fetch_all(query=locations.select().where(locations.c.chat_id == chat_id))
    elif work == 'get':
        return await database.fetch_one(query=locations.select().where(
            locations.c.location_name == location,
        ))
    elif work == 'add':
        if not await database.fetch_one(
                query=locations.select().where(locations.c.chat_id == chat_id, locations.c.location_name == location)):
            return await database.execute(query=locations.insert().values(
                location_name=location,
                latitude=f"{data['latitude']}a",
                longitude=f"{data['longitude']}a",
                chat_id=data['chat_id']
            ))


async def payments_settings(work=None, data=None, payment_name=None):
    if work == 'get':
        return await database.fetch_all(query=payments.select().where(payments.c.status == True))
    elif work == "false_payments":
        return await database.fetch_all(query=payments.select().where(payments.c.status == False))
    elif work == 'turn_off':
        return await database.execute(query=payments.update().values(
            status=False
        ).where(payments.c.payment_name == payment_name))
    elif work == "delete":
        return await database.execute(query=payments.delete().where(payments.c.payment_name == payment_name))
    elif work == "update":
        return await database.execute(query=payments.update().values(
            status=True
        ).where(payments.c.payment_name == payment_name))
    elif work == 'add':
        return await database.execute(query=payments.insert().values(
            payment_name=payment_name,
            status=True
        ))


async def curers_settings(work=None, data=None, chat_id=None):
    if work == 'get_not_working':
        return await database.fetch_one(query=curers.select().where(curers.c.status == 'Not Work'))
    elif work == 'get_all_curers':
        return await database.fetch_all(query=curers.select())
    elif work == 'delete':
        if str(data['name']).isdigit():
            return await database.execute(query=curers.delete().where(curers.c.chat_id == int(data['name'])))
        else:
            return await database.execute(query=curers.delete().where(curers.c.name == data['name']))
    elif work == "insert":
        return await database.execute(query=curers.insert().values(
            name=data['name'],
            chat_id=data['chat_id'],
            status='Not Work',
            is_working=False
        ))
    elif work == 'turn_off_status':
        return await database.execute(query=curers.update().values(is_working=False))
    elif work == 'turn_on_status':
        return await database.execute(query=curers.update().values(is_working=True))
    elif work == 'update':
        curer = await database.fetch_one(query=curers.select().where(curers.c.chat_id == chat_id))
        status = curer['status']
        if status == "Not Work":
            return await database.execute(query=curers.update().values(
                status='Working 1'
            ))
        else:
            number = status[-1]
            return await database.execute(query=curers.update().values(
                status=f"Working {int(number) + 1}"
            ))
    elif work == 'get':
        return await database.fetch_one(query=curers.select().where(curers.c.chat_id == chat_id))


async def logo_settings(work=None, photo=None):
    if work == "get":
        return await database.fetch_one(query=logo.select())
    elif work == 'update':
        if await database.fetch_one(query=logo.select()):
            return await database.execute(query=logo.update().values(
                photo=photo
            ))
        else:
            return await database.execute(query=logo.insert().values(
                photo=photo
            ))


async def settings(work=None, lang=None, phone_number=None, full_name=None, chat_id=None):
    if work == 'set_lang':
        return await database.execute(query=users.update().values(
            lang=lang
        ).where(users.c.chat_id == chat_id))
    elif work == 'set_number':
        return await database.execute(query=users.update().values(
            phone_number=phone_number
        ).where(users.c.chat_id == chat_id))
    elif work == "set_name":
        return await database.execute(query=users.update().values(
            full_name=full_name
        ).where(users.c.chat_id == chat_id))


async def add_product_to_basket(product, menu_name, narx, chat_id):
    amount = await database.fetch_one(
        query=foods_menu.select().where(foods_menu.c.name == product, foods_menu.c.menu == menu_name))
    if amount['is_have'] >= 1:
        await database.execute(query=basket.insert().values(
            product=product,
            menu_name=menu_name,
            miqdor=1,
            narx=narx,
            chat_id=chat_id
        ))
        return True
    else:
        return None


async def basket_settings(work=None, chat_id=None, product_name=None):
    if work == "get":
        return await database.fetch_all(query=basket.select().where(basket.c.chat_id == chat_id))
    elif work == "delete":
        return await database.execute(
            query=basket.delete().where(basket.c.chat_id == chat_id, basket.c.product == product_name))
    elif work == 'delete_basket':
        return await database.execute(query=basket.delete().where(basket.c.chat_id == chat_id))
