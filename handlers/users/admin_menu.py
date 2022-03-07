# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from keyboards.default import *
from keyboards.inline import choice_way_input_payment_func
from loader import dp, bot
from utils import get_dates
from utils.db_api.sqlite import *
from states.state_users import *
import json

# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ


def split_messages(get_list, count):
    return [get_list[i: i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Платежные системы"
@dp.message_handler(IsAdmin(), text="🔑 Платежные системы", state="*")
async def payments_systems(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "🔑 Настройка платежных системы.", reply_markup=payment_default()
    )
    await message.answer(
        "Выберите способ пополнения 💵\n"
        "\n"
        "🔸 <a href='https://vk.cc/bYjKGM'><b>По форме</b></a> - <code>Готовая форма оплаты QIWI</code>\n"
        "🔸 <a href='https://vk.cc/bYjKEy'><b>По номеру</b></a> - <code>Перевод средств по номеру телефона</code>\n"
        "🔸 <a href='https://vk.cc/bYjKJk'><b>По никнейму</b></a> - "
        "<code>Перевод средств по никнейму (пользователям придётся вручную вводить комментарий)</code>",
        reply_markup=choice_way_input_payment_func(),
    )


# Обработка кнопки "Настройки бота"
@dp.message_handler(IsAdmin(), text="⚙ Настройки", state="*")
async def settings_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⚙ Основные настройки бота.", reply_markup=get_settings_func())


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="🔆 Общие функции", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "🔆 Выберите нужную функцию.",
        reply_markup=get_functions_func(message.from_user.id),
    )


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="📰 Информация о боте", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    about_bot = get_about_bot()
    await message.answer(about_bot)


# Обработка кнопки "Управление товарами"
@dp.message_handler(IsAdmin(), text="🎁 Управление товарами 🖍", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "🎁 Редактирование товаров, разделов и категорий 📜", reply_markup=items_default
    )


# Получение БД
@dp.message_handler(IsAdmin(), text="/getbd", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    for admin in admins:
        with open("data/botBD.sqlite", "rb") as doc:
            await bot.send_document(
                admin, doc, caption=f"<b>📦 BACKUP</b>\n" f"<code>🕜 {get_dates()}</code>"
            )


def get_about_bot():
    (
        show_profit_all,
        show_profit_day,
        show_refill,
        show_buy_day,
        show_money_in_bot,
        show,
    ) = (0, 0, 0, 0, 0, 0)
    get_settings = get_settingsx()
    all_purchases = get_all_purchasesx()
    all_users = get_all_usersx()
    all_refill = get_all_refillx()
    show_users = get_all_usersx()
    show_categories = get_all_categoriesx()
    show_positions = get_all_positionsx()
    show_items = get_all_itemsx()
    for purchase in all_purchases:
        show_profit_all += int(purchase[6])
        if int(get_settings[4]) - int(purchase[14]) < 86400:
            show_profit_day += int(purchase[6])
    for user in all_users:
        show_money_in_bot += int(user[4])
    for refill in all_refill:
        show_refill += int(refill[5])
        if int(get_settings[5]) - int(refill[9]) < 86400:
            show_buy_day += int(refill[5])
    message = (
        "<b>📰 ВСЯ ИНФОРАМЦИЯ О БОТЕ</b>\n"
        f"\n"
        f"<b>🔶 Пользователи: 🔶</b>\n"
        f"👤 Пользователей: <code>{len(show_users)}</code>\n"
        f"\n"
        f"<b>🔶 Средства 🔶</b>\n"
        f"📗 Продаж за 24 часа на: <code>{show_profit_day}руб</code>\n"
        f"💰 Продано товаров на: <code>{show_profit_all}руб</code>\n"
        f"📕 Пополнений за 24 часа: <code>{show_buy_day}руб</code>\n"
        f"💳 Средств в системе: <code>{show_money_in_bot}руб</code>\n"
        f"💵 Пополнено: <code>{show_refill}руб</code>\n"
        f"\n"
        f"<b>🔶 Прочее 🔶</b>\n"
        f"🎁 Товаров: <code>{len(show_items)}</code>\n"
        f"📁 Позиций: <code>{len(show_positions)}</code>\n"
        f"📜 Категорий: <code>{len(show_categories)}</code>\n"
        f"🛒 Продано товаров: <code>{len(all_purchases)}</code>\n"
    )
    return message


# Получение списка всех товаров
@dp.message_handler(IsAdmin(), text="/getitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer(
            "<b>🎁 Все товары</b>\n"
            "\n"
            "<code>📍 айди товара - данные товара</code>\n"
            "\n"
        )
        for item in get_items:
            save_items.append(f"<code>📍 {item[1]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")


# Получение списка всех позиций
@dp.message_handler(IsAdmin(), text="/getposition", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_positionsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>📁 Все позиции</b>\n\n")
        for item in get_items:
            print(item)
            save_items.append(f"<code>{item[2]}</code>")
        if len_items >= 35:
            count_split = round(len_items / 35)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>📁 Позиции отсутствуют</b>")


# Получение подробного списка всех товаров
@dp.message_handler(IsAdmin(), text="/getinfoitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары и их позиции</b>\n" "\n")
        for item in get_items:
            get_position = get_positionx("*", position_id=item[3])
            save_items.append(f"<code>{get_position[2]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")


@dp.message_handler(IsAdmin(), text="💸 Зарплата", state="*")
async def get_chat_id31(message: types.Message, state: FSMContext):
    element_salary = []
    with open("salary.json") as f:
        data = json.load(f)

    price_admin = data["admin_cafe"]["salary"]
    price_admin1 = data["admin_cafe"]["sales"]

    price_ferrisWheel = data["ferrisWheel"]["salary"]
    price_ferrisWheel1 = data["ferrisWheel"]["sales"]

    price_laughingRoom = data["laughingRoom"]["salary"]
    price_laughingRoom1 = data["laughingRoom"]["sales"]

    price_carousel = data["carousel"]["salary"]
    price_carousel1 = data["carousel"]["sales"]

    blagotvoritelnost = (
        (price_admin + price_ferrisWheel + price_laughingRoom + price_carousel)
        // 100
        * 5
    )

    salary_sales = f"""
    
Администратор кафе
Заработано: {price_admin} руб
Продано товаров: {price_admin1}


Администратор аттракциона ( колесо обозрения )
Заработано: {price_ferrisWheel} руб
Продано товаров: {price_ferrisWheel1}


Администратор аттракциона ( комната смеха )
Заработано: {price_laughingRoom} руб
Продано товаров: {price_laughingRoom1}


Механик аттракционов (фиксированная зарплата за месяц)
Заработано: 20 000 руб

Общий заработок парка: {price_admin + price_ferrisWheel + price_laughingRoom + price_carousel - blagotvoritelnost}
Общее количество продаж: {price_admin1 + price_ferrisWheel1 + price_laughingRoom1 + price_carousel1}
Сумма которая уйдет на благотворительность в этом месяце: {blagotvoritelnost}

"""

    # await message.answer(salary_sales)
    await bot.send_photo(
        message.from_user.id,
        "https://www.gorno-altaisk.info/wp-content/uploads/2020/06/001-nga-206.jpg",
        caption=salary_sales,
    )

    await message.answer(
        """
Оператор парка (фиксированная зарплата за месяц)
Заработано: 25 000р


Кассир (фиксированная зарплата за месяц)
Заработано: 18 000р

Администратор (фиксированная зарплата за месяц)
Заработано: 35 000р

Инструктор (фиксированная зарплата за месяц)
Заработано: 20 000р

Фотограф (фиксированная зарплата за месяц)
Заработано: 20 000р

Аниматор (фиксированная зарплата за месяц)
Заработано: 20 000р

Повар (фиксированная зарплата за месяц)
Заработано: 30 000р

Официант (фиксированная зарплата за месяц)
Заработано: 18 000р

    """
    )


@dp.message_handler(IsAdmin(), text="📗 Добавить активность", state="*")
async def get_chat_id312(message: types.Message, state: FSMContext):
    await message.answer("✍ Напишите активность.")
    await StorageUsers.activity.set()


@dp.message_handler(IsAdmin(), state=StorageUsers.activity)
async def get_chat_id312(message: types.Message, state: FSMContext):
    await message.answer("✅ Готово")
    data = [message.text]
    with open("activities.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    await state.finish()


# 📕 Очистить посещения


@dp.message_handler(IsAdmin(), text="📕 Очистить посещения", state="*")
async def get_chat_id312(message: types.Message, state: FSMContext):
    await message.answer("✅ Готово")
    data = ["Посещение были очищены администратором"]
    with open("booking_park.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.message_handler(IsAdmin(), text="⚙ Добавить купон", state="*")
async def get_chdat_id3212(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите число пользователей которые смогут активировать купон:"
    )
    await StorageUsers.get_count_users_c.set()


@dp.message_handler(IsAdmin(), state=StorageUsers.get_count_users_c)
async def gets_chast_idda312(message: types.Message, state: FSMContext):
    global users_active_kupon
    users_active_kupon = int(message.text)
    await message.answer("Теперь введите сумму купона:")
    await StorageUsers.get_price_users_c.set()


@dp.message_handler(IsAdmin(), state=StorageUsers.get_price_users_c)
async def gets_chast_idda312(message: types.Message, state: FSMContext):
    global users_price_kupon
    users_price_kupon = int(message.text)
    await message.answer("Введите имя купона:")
    await StorageUsers.get_name_coupons_c.set()


@dp.message_handler(IsAdmin(), state=StorageUsers.get_name_coupons_c)
async def gets_chast_idda312(message: types.Message, state: FSMContext):
    name_coupons = message.text
    data1 = {}
    try:
        with open("coupons.json", encoding="utf-8") as file:
            data1 = json.load(file)
    except:
        pass
    data1[name_coupons] = {
        "count": users_active_kupon,
        "price": users_price_kupon,
        "tg_ids": str(message.from_user.id),
    }

    await state.finish()

    with open("coupons.json", "w") as file:
        json.dump(data1, file, indent=4, ensure_ascii=False)
