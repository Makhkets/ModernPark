# - *- coding: utf- 8 - *-

from ast import arg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.deep_linking import decode_payload

from data import config
from keyboards import *

from filters import IsWork, IsUser
from filters.all_filters import IsBuy
from keyboards.default import check_user_out_func
from loader import dp, bot
from states import StorageUsers
from utils.db_api.sqlite import *
from utils.other_func import clear_firstname, get_dates

import random
import string
import qrcode


prohibit_buy = [
    "xbuy_item",
    "not_buy_items",
    "buy_this_item",
    "buy_open_position",
    "back_buy_item_position",
    "buy_position_prevp",
    "buy_position_nextp",
    "buy_category_prevp",
    "buy_category_nextp",
    "back_buy_item_to_category",
    "buy_open_category",
]


# Проверка на нахождение бота на технических работах
@dp.message_handler(IsWork(), state="*")
@dp.callback_query_handler(IsWork(), state="*")
async def send_work_message(message: types.Message, state: FSMContext):
    if "id" in message:
        await message.answer("🔴 Бот находится на технических работах.")
    else:
        await message.answer("<b>🔴 Бот находится на технических работах.</b>")


def create_qrcode(url, name):
    qr = qrcode.make(data=url)
    qr.save(stream=f"qrcode/{name}.png")

    print("[+] QR-CODE was created")


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

# Обработка кнопки "На главную" и команды "/start"


@dp.message_handler(text="⬅ На главную", state="*")
@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    from loguru import logger
    await state.finish()
    x = generate_random_string(10)
    args = message.get_args()
    with sqlite3.connect(path_to_db) as db:
        users_info = db.execute(
            f"SELECT * FROM storage_users WHERE user_id = {message.from_user.id}").fetchall()

        qrcode_list = db.execute(
            f"SELECT qr_code FROM storage_users").fetchall()

    qrcode = []
    for i in qrcode_list:
        qrcode.append(i[0])

    if str(args) in qrcode:
        if str(message.from_user.id) in config.admins:
            logger.success("Вы админ")

            with sqlite3.connect(path_to_db) as db:
                get_user_data = db.execute(
                    f"SELECT user_login FROM storage_users WHERE qr_code = '{str(args)}'").fetchone()

            get_user_data = get_user_data[0]
            logger.success(get_user_data)
            get_user_id = get_userx(user_login=get_user_data.lower())
            if get_user_id is not None:
                await bot.send_photo(
                    message.from_user.id,
                    open(f"qrcode/{args}.png", "rb"),
                    caption=search_user_profile(get_user_id[1]),
                    reply_markup=search_profile_func(get_user_id[1]),
                )

                await state.finish()
            else:
                await message.answer("<b>❌ Профиль не был найден</b>\n"
                                     "📱 Введите логин или айди пользователя. Пример:\n")

            # вывод баланса карты бонуса
        if not(str(message.from_user.id) in config.admins):
            await bot.send_photo(
                message.from_user.id,
                open(f"qrcode/{args}.png", "rb"),
                caption=get_user_qrcode_profile(message.from_user.id),
                reply_markup=open_profile_inl,
            )

    if int(len(users_info)) == 0:
        create_qrcode(f"https://t.me/ModernPark_bot?start={x}", x)

    first_name = clear_firstname(message.from_user.first_name)
    get_user_id = get_userx(user_id=message.from_user.id)
    if get_user_id is None:
        if message.from_user.username is not None:
            get_user_login = get_userx(user_login=message.from_user.username)
            if get_user_login is None:
                add_userx(
                    message.from_user.id,
                    message.from_user.username.lower(),
                    first_name,
                    0,
                    0,
                    get_dates(),
                    x,
                )
            else:
                delete_userx(user_login=message.from_user.username)
                add_userx(
                    message.from_user.id,
                    message.from_user.username.lower(),
                    first_name,
                    0,
                    0,
                    get_dates(),
                    x,
                )
        else:
            add_userx(
                message.from_user.id,
                message.from_user.username,
                first_name,
                0,
                0,
                get_dates(),
                x,
            )
    else:
        if first_name != get_user_id[3]:
            update_userx(get_user_id[1], user_name=first_name)
        if message.from_user.username is not None:
            if message.from_user.username.lower() != get_user_id[2]:
                update_userx(
                    get_user_id[1], user_login=message.from_user.username.lower()
                )

    await message.answer(
        f"Добрый день, {message.from_user.first_name}! Мы рады приветствовать Вас в чат-боте парка\n«Modern Park»!\n\nДля выбора интересующего вас раздела воспользуйтесь кнопками из меню ниже 👇\n\n👁 Если вы не видите внизу кнопки меню, нажмите квадрат с 4-мя точкам правее окна ввода сообщений.",
        reply_markup=check_user_out_func(message.from_user.id),
    )


@dp.message_handler(IsUser(), state="*")
@dp.callback_query_handler(IsUser(), state="*")
async def send_user_message(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(
        message.from_user.id, "<b>❗ Ваш профиль не был найден.</b>\n" "▶ Введите /start"
    )


# Проверка на доступность покупок
@dp.message_handler(IsBuy(), text="🎁 Купить", state="*")
@dp.message_handler(IsBuy(), state=StorageUsers.here_input_count_buy_item)
@dp.callback_query_handler(IsBuy(), text_startswith=prohibit_buy, state="*")
async def send_user_message(message, state: FSMContext):
    if "id" in message:
        await message.answer("🔴 Покупки в боте временно отключены", True)
    else:
        await message.answer("<b>🔴 Покупки в боте временно отключены</b>")
