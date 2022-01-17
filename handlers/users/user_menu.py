# - *- coding: utf- 8 - *-
from logging import log
from os import remove
from aiogram.dispatcher.filters import state
from aiogram.types import ContentType, File, Message, callback_query, reply_keyboard
from pathlib import Path
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, message
from aiogram.types.base import Integer
from requests.api import get
import data
from keyboards import inline

from itertools import groupby
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_payment import StorageQiwi
from states.state_users import *
from utils.other_func import clear_firstname, get_dates
import configparser
import requests
from keyboards.default import all_back_to_main_default, check_user_out_func
from keyboards.inline import *
from loader import dp, bot
from states.state_payment import StorageQiwi
from utils import send_all_admin, clear_firstname, get_dates
from utils.db_api.sqlite import update_userx, get_refillx, add_refillx
import states
from keyboards import *
from keyboards import *
from loguru import logger
from pprint import pprint

config = configparser.ConfigParser()
config.read("settings.ini")
admin_id = config["settings"]["admin_cafe"]

# 382043304 - билеты


def split_messages(get_list, count):
    return [get_list[i: i + count] for i in range(0, len(get_list), count)]


######################################################################################################################


@dp.callback_query_handler(text_startswith="napitki_menu", state="*")
async def open_category_fosr_buy_item(call: CallbackQuery, state: FSMContext):
    try:
        global position_ids_napitki
        global remover
        global user_id_menu
        global category_id_napitki

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_napitki"])

        position_ids_napitki = [
            "852138731",
            "718707976",
            "221989525",
            "409004636",
            "850205332",
            "973543653",
        ]

        position_id = position_ids_napitki[count]
        remover = 0
        category_id_napitki = "973954286"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_napitki)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items) } шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_napitki(
                    position_id, remover, category_id_napitki
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_napitki(
                    position_id, remover, category_id_napitki
                ),
            )
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[user_id_menu] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_napitki"])

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_napitki)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_napitki(
                    position_id, remover, category_id_napitki
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_napitki(
                    position_id, remover, category_id_napitki
                ),
            )


@dp.callback_query_handler(text_startswith="next_napitki", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_napitki"])

    count += 1

    if count >= len(position_ids_napitki):
        count = 0

    position_id = position_ids_napitki[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_napitki)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_napitki(
                position_id, remover, category_id_napitki
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_napitki(
                position_id, remover, category_id_napitki
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": "0",
        "count_menu_sushi": "0",
        "count_menu_napitki": str(count),
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back_napitki", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_napitki"])

    count -= 1

    if count <= 0:
        count = 1

    position_id = position_ids_napitki[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_napitki)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_napitki(
                position_id, remover, category_id_napitki
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_napitki(
                position_id, remover, category_id_napitki
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": "0",
        "count_menu_sushi": "0",
        "count_menu_napitki": str(count),
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


######################################################################################################################


@dp.callback_query_handler(text_startswith="sushi_menu", state="*")
async def open_category_fosr_buy_item(call: CallbackQuery, state: FSMContext):
    try:
        global position_ids_sushi
        global remover
        global user_id_menu
        global category_id_sushi

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_sushi"])

        position_ids_sushi = ["874616236", "377374060", "993999821"]

        position_id = position_ids_sushi[count]
        remover = 0
        category_id_sushi = "738309413"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_sushi)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_sushi(
                    position_id, remover, category_id_sushi
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_sushi(
                    position_id, remover, category_id_sushi
                ),
            )
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[user_id_menu] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_sushi"])

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_sushi)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_sushi(
                    position_id, remover, category_id_sushi
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_sushi(
                    position_id, remover, category_id_sushi
                ),
            )


@dp.callback_query_handler(text_startswith="next_sushi", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_sushi"])

    count += 1

    if count >= len(position_ids_sushi):
        count = 0

    position_id = position_ids_sushi[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_sushi)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_sushi(
                position_id, remover, category_id_sushi
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_sushi(
                position_id, remover, category_id_sushi
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": "0",
        "count_menu_sushi": str(count),
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back_sushi", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_sushi"])

    count -= 1

    if count <= 0:
        count = 1

    position_id = position_ids_sushi[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_sushi)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_sushi(
                position_id, remover, category_id_sushi
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_sushi(
                position_id, remover, category_id_sushi
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": "0",
        "count_menu_sushi": str(count),
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


######################################################################################################################


@dp.callback_query_handler(text_startswith="pizza_menu", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    try:
        global position_ids_pizza
        global remover
        global user_id_menu
        global category_id_pizza

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_pizza"])

        position_ids_pizza = ["921677285", "536446876", "422077533"]

        position_id = position_ids_pizza[count]
        remover = 0
        category_id_pizza = "738309413"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_pizza)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_pizza(
                    position_id, remover, category_id_pizza
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_pizza(
                    position_id, remover, category_id_pizza
                ),
            )
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[user_id_menu] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_pizza"])

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_pizza)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_pizza(
                    position_id, remover, category_id_pizza
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_pizza(
                    position_id, remover, category_id_pizza
                ),
            )


@dp.callback_query_handler(text_startswith="next_pizza", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_pizza"])

    count += 1

    if count >= len(position_ids_pizza):
        count = 0

    position_id = position_ids_pizza[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_pizza)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_pizza(
                position_id, remover, category_id_pizza
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_pizza(
                position_id, remover, category_id_pizza
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": str(count),
        "count_menu_sushi": "0",
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back_pizza", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_pizza"])

    count -= 1

    if count <= 0:
        count = 1

    position_id = position_ids_pizza[count]
    remover = 0

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_pizza)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_pizza(
                position_id, remover, category_id_pizza
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_pizza(
                position_id, remover, category_id_pizza
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": str(count),
        "count_menu_sushi": "0",
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


######################################################################################################################


@dp.callback_query_handler(text_startswith="burger_menu", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    try:
        global position_ids_burger
        global remover
        global user_id_menu
        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_burger"])

        position_ids_burger = ["871614372", "922748873", "429866361"]

        position_id = position_ids_burger[count]
        remover = 0
        category_id_burger = "328691982"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_burger)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_burger(
                    position_id, remover, category_id_burger
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_burger(
                    position_id, remover, category_id_burger
                ),
            )
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[user_id_menu] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_burger"])

        position_ids_burger = ["871614372", "922748873", "429866361"]

        position_id = position_ids_burger[count]
        remover = 0
        category_id_burger = "328691982"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_burger)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_burger(
                    position_id, remover, category_id_burger
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_burger(
                    position_id, remover, category_id_burger
                ),
            )


@dp.callback_query_handler(text_startswith="next_burger", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_burger"])

    count += 1

    if count >= len(position_ids_burger):
        count = 0

    position_id = position_ids_burger[count]
    remover = 0
    category_id_burger = "328691982"

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_burger)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_burger(
                position_id, remover, category_id_burger
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_burger(
                position_id, remover, category_id_burger
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": str(count),
        "count_menu_pizza": "0",
        "count_menu_sushi": "0",
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back_burger", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_burger"])

    count -= 1

    if count <= 0:
        count = 1

    position_id = position_ids_burger[count]
    remover = 0
    category_id_burger = "328691982"

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_burger)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт./code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_burger(
                position_id, remover, category_id_burger
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_tickets(
                position_id, remover, category_id_burger
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": "0",
        "count_menu_burger": "0",
        "count_menu_pizza": str(count),
        "count_menu_sushi": "0",
        "count_menu_napitki": "0",
        "count_tickets_menu_st": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


#######################################################################################################################


@dp.callback_query_handler(text_startswith="ticket_menu", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    try:
        global position_ids_ticket
        global remover
        global user_id_menu
        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_ticket"])

        position_ids_ticket = ["692734953",
                               "536244465", "865769734", "915515566"]

        position_id = position_ids_ticket[count]
        remover = 0
        category_id_ticket = "382043304"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_ticket)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_tickets(
                    position_id, remover, category_id_ticket
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_tickets(
                    position_id, remover, category_id_ticket
                ),
            )
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[user_id_menu] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        user_id_menu = str(call.message.chat.id)

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[user_id_menu]["count_menu_ticket"])

        position_ids_ticket = ["692734953",
                               "536244465", "865769734", "915515566"]

        position_id = position_ids_ticket[count]
        remover = 0
        category_id_ticket = "382043304"

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id_ticket)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func_menu_tickets(
                    position_id, remover, category_id_ticket
                ),
            )
        else:
            await call.message.edit_text(
                send_msg,
                reply_markup=open_item_func_menu_tickets(
                    position_id, remover, category_id_ticket
                ),
            )


@dp.callback_query_handler(text_startswith="next_ticket", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_ticket"])

    count += 1

    if count >= len(position_ids_ticket):
        count = 0

    position_id = position_ids_ticket[count]
    remover = 0
    category_id_ticket = "382043304"

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_ticket)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_tickets(
                position_id, remover, category_id_ticket
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_tickets(
                position_id, remover, category_id_ticket
            ),
        )

    data[user_id_menu] = {
        "count": "0",
        "count_menu_ticket": str(count),
        "count_menu_burger": "0",
    }

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back_ticket", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[user_id_menu]["count_menu_ticket"])

    count -= 1

    if count <= 0:
        count = 1

    position_id = position_ids_ticket[count]
    remover = 0
    category_id_ticket = "382043304"

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id_ticket)

    get_items = get_itemsx("*", position_id=position_id)

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n"
        f"\n"
        f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
        f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
        f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup=open_item_func_menu_tickets(
                position_id, remover, category_id_ticket
            ),
        )
    else:
        await call.message.edit_text(
            send_msg,
            reply_markup=open_item_func_menu_tickets(
                position_id, remover, category_id_ticket
            ),
        )

    data[user_id_menu] = {"count": "0", "count_menu_ticket": str(count)}

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


############################################################################################################################


@dp.message_handler(text="📓 Меню ресторана", state="*")
async def gewt_chfsdsdat_id2(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    with open("images/menu.mp4", "rb") as video:
        await message.answer_video(video, reply_markup=menu_category)

    # await bot.send_photo(
    #     message.chat.id,
    #     "http://restaurant-benefis.ru/wp-content/uploads/2019/09/IMG-20190925-WA0026-1024x683.jpg",
    #     "Выберите категорию",
    #     reply_markup=menu_category,
    # )
    # await bot.send_video


@dp.callback_query_handler(text_startswith="menu_shop", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_photo(
        call.message.chat.id,
        "https://i.imgur.com/z0RNYip.jpg",
        reply_markup=menu_category,
    )


# https://www.klass39.ru/wp-content/uploads/2012/04/7d69e357a9267fc119efde2caf423862-750x375.jpg


# Обработка кнопки "Купить"
@dp.message_handler(text="🎁 Покупка", state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
    get_categories = get_all_categoriesx()
    if len(get_categories) >= 1:
        get_kb = buy_item_open_category_ap(0)
        await message.answer("<b>Выберите нужный вам товар:</b>", reply_markup=get_kb)
    else:
        await message.answer("<b>🎁 Товары в данное время отсутствуют.</b>")


# Обработка кнопки "Профиль"
@dp.message_handler(text="📱 Профиль", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        get_user_profile(message.from_user.id), reply_markup=open_profile_inl
    )


# Обработка кнопки "FAQ"
@dp.message_handler(text="ℹ FAQ", state="*")
async def show_my_deals(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    send_msg = get_settings[1]
    if "{username}" in send_msg:
        send_msg = send_msg.replace(
            "{username}", f"<b>{message.from_user.username}</b>"
        )
    if "{user_id}" in send_msg:
        send_msg = send_msg.replace(
            "{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in send_msg:
        send_msg = send_msg.replace(
            "{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>"
        )
    await bot.send_photo(
        message.from_user.id,
        "https://www.dvfu.ru/education/online-training/f-a-q/FAQ.png",
        send_msg,
    )


# Обработка кнопки "Поддержка"
@dp.message_handler(text="📕 Поддержка", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    await bot.send_photo(
        message.from_user.id,
        "https://www.sacmi.com/SacmiCorporate/media/Corporate/Default%20Pict/Form-contatti_2-3.jpg",
        get_settings[0],
    )


global pucrh
global productsz

# Обработка колбэка "Мои покупки"


@dp.message_handler(text="🔍 Меню", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await message.answer_photo(
        "https://scontent-arn2-1.cdninstagram.com/v/t51.2885-15/e35/106299819_270501910957866_3663256566949371216_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_cat=106&_nc_ohc=XjtpeSxEobcAX8PUZTJ&edm=AABBvjUBAAAA&ccb=7-4&oh=00_AT9OcdddsO_3fm0E3Y63Q04oil9KRDQ66g2pUJ6u7S7aGQ&oe=61E20AA2&_nc_sid=83d603",
        "Будем ждать Вас в гости!",
        reply_markup=menu_category_,
    )
    # await message.answer_location(43.345857, 45.640887, reply_markup=menu_category_)
    # await message.answer("Будем ждать Вас в гости!")


@dp.callback_query_handler(text="my_buy", state="*")
async def show_referral(call: CallbackQuery, state: FSMContext):
    last_purchases = last_purchasesx(call.from_user.id)
    if len(last_purchases) >= 1:
        await call.message.delete()
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(
                f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]}руб\n"
                f"🕜 {purchases[13]}\n"
                f"<code>{purchases[10]}</code>"
            )

        await call.message.answer("<b>🛒 Последние 10 покупок</b>\n" "")
        save_purchases.reverse()
        len_purchases = len(save_purchases)

        # не трогай ничего

        # Инлайн клавиатура
        inlineh1 = InlineKeyboardMarkup()
        inlineh1.add(
            InlineKeyboardButton("🟢  Активировать билет 1",
                                 callback_data="one1")
        )

        inlineh2 = InlineKeyboardMarkup()
        inlineh2.add(
            InlineKeyboardButton("🟢  Активировать билет 2",
                                 callback_data="one2")
        )

        inlineh3 = InlineKeyboardMarkup()
        inlineh3.add(
            InlineKeyboardButton("🟢  Активировать билет 3",
                                 callback_data="one3")
        )

        inlineh4 = InlineKeyboardMarkup()
        inlineh4.add(
            InlineKeyboardButton("🟢  Активировать билет 4",
                                 callback_data="one4")
        )

        inlineh5 = InlineKeyboardMarkup()
        inlineh5.add(
            InlineKeyboardButton("🟢  Активировать билет 5",
                                 callback_data="one5")
        )

        inlineh6 = InlineKeyboardMarkup()
        inlineh6.add(
            InlineKeyboardButton("🟢  Активировать билет 6",
                                 callback_data="one6")
        )

        inlineh7 = InlineKeyboardMarkup()
        inlineh7.add(
            InlineKeyboardButton("🟢  Активировать билет 7",
                                 callback_data="one7")
        )

        inlineh8 = InlineKeyboardMarkup()
        inlineh8.add(
            InlineKeyboardButton("🟢  Активировать билет 8",
                                 callback_data="one8")
        )

        inlineh9 = InlineKeyboardMarkup()
        inlineh9.add(
            InlineKeyboardButton("🟢  Активировать билет 9",
                                 callback_data="one9")
        )

        inlineh10 = InlineKeyboardMarkup()
        inlineh10.add(
            InlineKeyboardButton(
                "🟢  Активировать билет 10", callback_data="one10")
        )

        global productsz
        productsz = []
        x = 1
        for i in save_purchases:
            if x == 1:
                await call.message.answer(i, reply_markup=inlineh1)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 2:
                await call.message.answer(i, reply_markup=inlineh2)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 3:
                await call.message.answer(i, reply_markup=inlineh3)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 4:
                await call.message.answer(i, reply_markup=inlineh4)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 5:
                await call.message.answer(i, reply_markup=inlineh5)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 6:
                await call.message.answer(i, reply_markup=inlineh6)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 7:
                await call.message.answer(i, reply_markup=inlineh7)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 8:
                await call.message.answer(i, reply_markup=inlineh8)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 9:
                await call.message.answer(i, reply_markup=inlineh9)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            elif x == 10:
                await call.message.answer(i, reply_markup=inlineh10)
                hash_code = i.split("<code>")[1].split("</code>")[0]
                productsz.append(hash_code)

            x += 1

        from loguru import logger

        logger.debug(productsz)
        try:
            productsz = [el for el, _ in groupby(x)]
        except:
            pass
        logger.success(productsz)

        await call.message.answer(
            get_user_profile(call.from_user.id), reply_markup=open_profile_inl
        )


################################################################################################
#####################################ОБРАБОТКА КАЛЛДАТЫ#########################################
@dp.callback_query_handler(lambda c: c.data == "one1")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[0]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one2")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[1]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one3")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[2]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one4")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[3]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one5")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[4]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one6")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[5]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one7")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[6]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one8")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[7]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one9")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[8]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


@dp.callback_query_handler(lambda c: c.data == "one10")
async def callbackone(callback_query: types.CallbackQuery):
    from loguru import logger

    clqq = productsz[9]
    clqq = clqq.replace("#", "")
    user_id = callback_query.from_user.id
    conn = sqlite3.connect(r"C:\Users\Fayli\Desktop\main\data\botBD.sqlite")
    cur = conn.cursor()
    logger.error(clqq)
    cur.execute("DELETE FROM storage_purchases WHERE receipt=?", (clqq,))
    conn.commit()
    await bot.send_message(user_id, "Действие выполнено")


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки


@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    get_category = get_categoryx("*", category_id=category_id)
    get_positions = get_positionsx("*", category_id=category_id)

    get_kb = buy_item_item_position_ap(0, category_id)
    if len(get_positions) >= 1:
        await call.message.edit_text(
            "<b>Выберите нужный вам товар</b>", reply_markup=get_kb
        )
    else:
        await call.answer(f"❕ Товары в категории {get_category[2]} отсутствуют.")


# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy_item_to_category", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "<b>Выберите нужный вам товар</b>", reply_markup=buy_item_open_category_ap(0)
    )


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>Выберите нужный вам товар</b>",
        reply_markup=buy_item_next_page_category_ap(remover),
    )


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>Выберите нужный вам товар</b>",
        reply_markup=buy_item_previous_page_category_ap(remover),
    )


# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>Выберите нужный вам товар:</b>",
        reply_markup=item_buy_next_page_position_ap(remover, category_id),
    )


# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>Выберите нужный вам товар</b>",
        reply_markup=item_buy_previous_page_position_ap(remover, category_id),
    )


# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.delete()
    await call.message.answer(
        "<b>Выберите нужный вам товар</b>",
        reply_markup=buy_item_item_position_ap(remover, category_id),
    )


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])

    logger.success(
        f"position_id {position_id} | remover {remover} | category_id {category_id}"
    )

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id)
    get_items = get_itemsx("*", position_id=position_id)

    if "🎫 Билеты на аттракцион" in get_category[2]:

        category_id_ticket = "382043304"

        get_positions = get_positionsx("*", category_id=category_id_ticket)
        global ids_tikckets_alls
        ids_tikckets_alls = []

        for i in get_positions:
            ids_tikckets_alls.append(i[1])

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()

            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=menu_ticketov(position_id, remover, category_id),
            )

        else:
            await call.message.edit_text(
                send_msg, reply_markup=menu_ticketov(
                    position_id, remover, category_id)
            )

    elif "Бронирование" in get_category[2]:

        get_positions = get_positionsx("*", category_id=category_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()

            with open("images/booking.mp4", "rb") as video:
                await call.message.answer_video(
                    video,
                    caption=send_msg,
                    reply_markup=open_item_func(
                        position_id, remover, category_id),
                )

        else:
            await call.message.edit_text(
                send_msg, reply_markup=open_item_func(
                    position_id, remover, category_id)
            )

    else:

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=open_item_func(
                    position_id, remover, category_id)
            )


@dp.callback_query_handler(text_startswith="nks", state="*")
async def opens_categorysfor_buy_item(call: CallbackQuery, state: FSMContext):
    """Кнопка вперед"""

    try:
        remover = 0

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        ids_menu_tickets_js = str(call.message.chat.id)

        count_js_menu_tickets = data[ids_menu_tickets_js]["count_tickets_menu_st"]

        if int(count_js_menu_tickets) >= len(ids_tikckets_alls):
            count_js_menu_tickets = "0"

        position_id = ids_tikckets_alls[int(count_js_menu_tickets)]

        remover = 0
        category_id = 382043304

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)
        get_items = get_itemsx("*", position_id=position_id)

        get_positions = get_positionsx("*", category_id=category_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=menu_ticketov(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=menu_ticketov(
                    position_id, remover, category_id)
            )

        counts_sdadsadas = int(count_js_menu_tickets) + 1

        data[ids_menu_tickets_js] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": str(counts_sdadsadas),
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except:
        with open("count.json", "r", encoding="utf-8") as fi:
            ss = json.load(fi)

        ss[str(call.message.chat.id)] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(ss, f, indent=4, ensure_ascii=False)

        remover = 0

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        ids_menu_tickets_js = str(call.message.chat.id)

        count_js_menu_tickets = data[ids_menu_tickets_js]["count_tickets_menu_st"]

        if int(count_js_menu_tickets) >= len(ids_tikckets_alls):
            count_js_menu_tickets = "0"

        position_id = ids_tikckets_alls[int(count_js_menu_tickets)]

        remover = 0
        category_id = 382043304

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)
        get_items = get_itemsx("*", position_id=position_id)

        get_positions = get_positionsx("*", category_id=category_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=menu_ticketov(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=menu_ticketov(
                    position_id, remover, category_id)
            )

        counts_sdadsadas = int(count_js_menu_tickets) + 1

        data[ids_menu_tickets_js] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": str(counts_sdadsadas),
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="bks", state="*")
async def opens_categorysfor_buy_item(call: CallbackQuery, state: FSMContext):
    """Кнопка вперед"""

    try:
        remover = 0

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        ids_menu_tickets_js = str(call.message.chat.id)

        count_js_menu_tickets = data[ids_menu_tickets_js]["count_tickets_menu_st"]

        if int(count_js_menu_tickets) <= 0:
            count_js_menu_tickets = "0"

        position_id = ids_tikckets_alls[int(count_js_menu_tickets)]

        remover = 0
        category_id = 382043304

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)
        get_items = get_itemsx("*", position_id=position_id)

        get_positions = get_positionsx("*", category_id=category_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=menu_ticketov(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=menu_ticketov(
                    position_id, remover, category_id)
            )

        counts_sdadsadas = int(count_js_menu_tickets) - 1

        data[ids_menu_tickets_js] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": str(counts_sdadsadas),
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except:
        with open("count.json", "r", encoding="utf-8") as fi:
            ss = json.load(fi)

        ss[str(call.message.chat.id)] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": "0",
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(ss, f, indent=4, ensure_ascii=False)

        remover = 0

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        ids_menu_tickets_js = str(call.message.chat.id)

        count_js_menu_tickets = data[ids_menu_tickets_js]["count_tickets_menu_st"]

        if int(count_js_menu_tickets) >= len(ids_tikckets_alls):
            count_js_menu_tickets = "0"

        position_id = ids_tikckets_alls[int(count_js_menu_tickets)]

        remover = 0
        category_id = 382043304

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)
        get_items = get_itemsx("*", position_id=position_id)

        get_positions = get_positionsx("*", category_id=category_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=menu_ticketov(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=menu_ticketov(
                    position_id, remover, category_id)
            )

        counts_sdadsadas = int(count_js_menu_tickets) + 1

        data[ids_menu_tickets_js] = {
            "count": "0",
            "count_menu_ticket": "0",
            "count_menu_burger": "0",
            "count_menu_pizza": "0",
            "count_menu_sushi": "0",
            "count_menu_napitki": "0",
            "count_tickets_menu_st": str(counts_sdadsadas),
        }

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    voice = await message.voice.get_file()
    path = "/files/voices"

    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)


# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    if len(get_items) >= 1:
        if int(get_user[4]) >= int(get_position[3]):
            async with state.proxy() as data:
                data["here_cache_position_id"] = position_id
            await call.message.delete()
            await StorageUsers.here_input_count_buy_item.set()
            await call.message.answer(
                f"📦 <b>Введите количество товаров для покупки</b>\n"
                f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                f"\n"
                f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n"
                f"💳 Ваш баланс: <code>{get_user[4]}руб</code>\n",
                reply_markup=all_back_to_main_default,
            )
        else:
            await call.answer("❗ У вас недостаточно средств. Пополните баланс")
    else:
        await call.answer("🎁 Товаров нет в наличии.")


# Принятие кол-ва товаров для покупки

@dp.message_handler(state=StorageUsers.here_input_count_buy_item)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = int(get_position[3]) * get_count
        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user[4]) >= amount_pay:
                    await state.finish()
                    delete_msg = await message.answer(
                        "<b>🎁 Товары подготовлены.</b>",
                        reply_markup=check_user_out_func(message.from_user.id),
                    )

                    await message.answer(
                        f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                        f"\n"
                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                        f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n"
                        f"\n"
                        f"▶ Количество товаров: <code>{get_count}шт</code>\n"
                        f"💰 Сумма к покупке: <code>{amount_pay}руб</code>",
                        reply_markup=confirm_buy_items(
                            position_id, get_count, delete_msg.message_id
                        ),
                    )
                else:
                    await message.answer(
                        f"<b>❌ Недостаточно средств на счете.</b>\n"
                        f"<b>📦 Введите количество товаров для покупки</b>\n"
                        f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                        f"\n"
                        f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                        f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
                        reply_markup=all_back_to_main_default,
                    )
            else:
                await message.answer(
                    f"<b>❌ Неверное количество товаров.</b>\n"
                    f"<b>📦 Введите количество товаров для покупки</b>\n"
                    f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                    f"\n"
                    f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                    f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                    f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
                    reply_markup=all_back_to_main_default,
                )
        else:
            await state.finish()
            await message.answer(
                "<b>🎁 Товар который вы хотели купить, закончился</b>",
                reply_markup=check_user_out_func(message.from_user.id),
            )
    else:
        await message.answer(
            f"<b>❌ Данные были введены неверно</b>\n"
            f"<b>📦 Введите количество товаров для покупки</b>\n"
            f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
            f"\n"
            f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
            f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
            reply_markup=all_back_to_main_default,
        )


# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await call.message.delete()
    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.answer(
        "<b>☑ Вы отменили покупку товаров.</b>",
        reply_markup=check_user_out_func(call.from_user.id),
    )


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    delete_msg = await call.message.answer("<b>🔄 Ждите, товары подготавливаются</b>")
    position_id = int(call.data.split(":")[1])
    get_count = int(call.data.split(":")[2])
    message_id = int(call.data.split(":")[3])

    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.delete()

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    amount_pay = int(get_position[3]) * get_count

    if 1 <= int(get_count) <= len(get_items):
        if int(get_user[4]) >= amount_pay:
            save_items, send_count, split_len = buy_itemx(get_items, get_count)

            if split_len <= 50:
                split_len = 70
            elif split_len <= 100:
                split_len = 50
            elif split_len <= 150:
                split_len = 30
            elif split_len <= 200:
                split_len = 10
            else:
                split_len = 3

            if get_count != send_count:
                amount_pay = int(get_position[3]) * send_count
                get_count = send_count

            random_number = [random.randint(100000000, 999999999)]
            passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
            random.shuffle(passwd)
            random_char = "".join([random.choice(passwd) for x in range(1)])
            receipt = random_char + str(random_number[0])
            buy_time = get_dates()

            await bot.delete_message(call.from_user.id, delete_msg.message_id)

            if len(save_items) <= split_len:
                send_message = "\n".join(save_items)
                await call.message.answer(
                    f"<b>🎁 Ваши товары:</b>\n" f"\n" f"{send_message}"
                )
            else:
                await call.message.answer(f"<b>🎁 Ваши товары:</b>\n" f"")

                save_split_items = split_messages(save_items, split_len)
                for item in save_split_items:
                    send_message = "\n".join(item)
                    await call.message.answer(send_message)
            save_items = "\n".join(save_items)

            add_purchasex(
                call.from_user.id,
                call.from_user.username,
                call.from_user.first_name,
                receipt,
                get_count,
                amount_pay,
                get_position[3],
                get_position[1],
                get_position[2],
                save_items,
                get_user[4],
                int(get_user[4]) - amount_pay,
                buy_time,
                int(time.time()),
            )
            update_userx(call.from_user.id, balance=get_user[4] - amount_pay)
            await call.message.answer(
                f"<b>🎁 Вы успешно купили товар(ы) ✅</b>\n"
                f"\n"
                f"📃 Чек: <code>#{receipt}</code>\n"
                f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                f"📦 Куплено товаров: <code>{get_count}</code>\n"
                f"💵 Сумма покупки: <code>{amount_pay}руб</code>\n"
                f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                f"🕜 Дата покупки: <code>{buy_time}</code>",
                reply_markup=check_user_out_func(call.from_user.id),
            )

            chat_id_org = config["settings"]["admin_cafe"]
            bot_tok = config["settings"]["token"]
            order_group = config["settings"]["orders_idGroup"]

            with open("salary.json") as f:
                read_file = json.load(f)

            if "Забронировать место" in get_position[2]:
                r = requests.get(
                    f"https://api.telegram.org/bot{bot_tok}/sendMessage?chat_id={chat_id_org}&text=⚡ У вас забронировали {get_count} места ⚡"
                )
                sales = int(read_file["admin_cafe"]["sales"])
                salary = int(read_file["admin_cafe"]["salary"])
                booking = {}
                read_file["admin_cafe"] = booking["admin_cafe"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)
                await call.message.answer(
                    "<b>Введите время когда придете в наше заведение</b>"
                )
                await StorageUsers.bronirovanie.set()

            elif "Коктель" in get_position[2]:
                await bot.send_message(
                    order_group,
                    f"📃 Чек: #{receipt}\n🏷 Название товара: {get_position[2]}\n📦 Куплено товаров: {get_count}\n💵 Сумма покупки: {amount_pay}руб\n👤 Покупатель: {get_user[3]}\n🕜 Дата покупки: {buy_time}\n\n🔴 НЕ ЗАБУДЬТЕ АКТИВИРОВАТЬ БИЛЕТ ПРИ ВЫДАЧЕ БЛЮДА",
                )
                sales = int(read_file["admin_cafe"]["sales"])
                salary = int(read_file["admin_cafe"]["salary"])
                booking1 = {}
                read_file["admin_cafe"] = booking1["admin_cafe"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)

            elif "Пицца" in get_position[2]:
                await bot.send_message(
                    order_group,
                    f"📃 Чек: #{receipt}\n🏷 Название товара: {get_position[2]}\n📦 Куплено товаров: {get_count}\n💵 Сумма покупки: {amount_pay}руб\n👤 Покупатель: {get_user[3]}\n🕜 Дата покупки: {buy_time}\n\n🔴 НЕ ЗАБУДЬТЕ АКТИВИРОВАТЬ БИЛЕТ ПРИ ВЫДАЧЕ БЛЮДА",
                )
                sales = int(read_file["admin_cafe"]["sales"])
                salary = int(read_file["admin_cafe"]["salary"])
                booking2 = {}
                read_file["admin_cafe"] = booking2["admin_cafe"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)

            elif "Бургер" in get_position[2]:
                await bot.send_message(
                    order_group,
                    f"📃 Чек: #{receipt}\n🏷 Название товара: {get_position[2]}\n📦 Куплено товаров: {get_count}\n💵 Сумма покупки: {amount_pay}руб\n👤 Покупатель: {get_user[3]}\n🕜 Дата покупки: {buy_time}\n\n🔴 НЕ ЗАБУДЬТЕ АКТИВИРОВАТЬ БИЛЕТ ПРИ ВЫДАЧЕ БЛЮДА",
                )
                sales = int(read_file["admin_cafe"]["sales"])
                salary = int(read_file["admin_cafe"]["salary"])
                booking3 = {}
                read_file["admin_cafe"] = booking3["admin_cafe"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)
            elif "Суши" in get_position[2]:
                await bot.send_message(
                    order_group,
                    f"📃 Чек: #{receipt}\n🏷 Название товара: {get_position[2]}\n📦 Куплено товаров: {get_count}\n💵 Сумма покупки: {amount_pay}руб\n👤 Покупатель: {get_user[3]}\n🕜 Дата покупки: {buy_time}\n\n🔴 НЕ ЗАБУДЬТЕ АКТИВИРОВАТЬ БИЛЕТ ПРИ ВЫДАЧЕ БЛЮДА",
                )
                sales = int(read_file["admin_cafe"]["sales"])
                salary = int(read_file["admin_cafe"]["salary"])
                booking4 = {}
                read_file["admin_cafe"] = booking4["admin_cafe"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)

            elif "Колесо обозрения" in get_position[2]:
                sales = int(read_file["ferrisWheel"]["sales"])
                salary = int(read_file["ferrisWheel"]["salary"])
                booking4 = {}
                read_file["ferrisWheel"] = booking4["ferrisWheel"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)

            elif "Комната смеха" in get_position[2]:
                sales = int(read_file["laughingRoom"]["sales"])
                salary = int(read_file["laughingRoom"]["salary"])
                booking4 = {}
                read_file["laughingRoom"] = booking4["laughingRoom"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)

            elif "Карусель" in get_position[2]:
                sales = int(read_file["carousel"]["sales"])
                salary = int(read_file["carousel"]["salary"])
                booking4 = {}
                read_file["carousel"] = booking4["carousel"] = {
                    "salary": amount_pay + salary,
                    "sales": get_count + sales,
                }
                with open("salary.json", "w") as file:
                    json.dump(read_file, file, indent=4, ensure_ascii=False)
        else:
            await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
    else:
        await state.finish()
        await call.message.answer(
            "<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
            check_user_out_func(call.from_user.id),
        )


# бронирование, сбор информации


@dp.message_handler(state=StorageUsers.bronirovanie)
async def show_search(message: types.Message, state: FSMContext):
    visit_time = message.text
    await bot.send_message(admin_id, f"<b>У вас забронировали место в {visit_time}</b>")
    await message.answer("<b>Теперь введите ваше имя</b>")
    await StorageUsers.bronirovanie2.set()


@dp.message_handler(state=StorageUsers.bronirovanie2)
async def show_search(message: types.Message, state: FSMContext):
    visit_name = message.text
    await bot.send_message(admin_id, f"Имя: {visit_name}")
    await message.answer("Анкета успешна отправлена")


@dp.message_handler(text="💰 Доплата наличными", state="*")
async def showasdf_searcsdh(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите сумму которую хотите обналичить со счета</b>")

    await StorageQiwi.balance_input_minus.set()
    state.fi


@dp.message_handler(state=StorageQiwi.balance_input_minus)
async def showasdf_searcsdh(message: types.Message, state: FSMContext):
    suma = int(message.text)
    get_user = get_userx(user_id=message.from_user.id)
    update_userx(message.from_user.id, balance=int(get_user[4]) - suma)

    await message.answer("Успешная оплата")
    await state.finish()


@dp.message_handler(text="💵 Пополнение баланса", state="*")
async def show_search(message: types.Message, state: FSMContext):
    await message.answer("Используйте кнопки управления", reply_markup=oplata_s)


@dp.message_handler(text="💵 Оплата киви", state="*")
async def show_search(message: types.Message, state: FSMContext):
    check_pass = False
    get_payment = get_paymentx()
    if get_payment[5] == "True":
        if (
            get_payment[0] != "None"
            and get_payment[1] != "None"
            and get_payment[2] != "None"
        ):
            try:
                request = requests.Session()
                request.headers["authorization"] = "Bearer " + get_payment[1]
                response_qiwi = request.get(
                    f"https://edge.qiwi.com/payment-history/v2/persons/{get_payment[0]}/payments",
                    params={"rows": 1, "operation": "IN"},
                )
                if response_qiwi.status_code == 200:
                    await StorageQiwi.here_input_qiwi_amount.set()
                    await bot.delete_message(message.from_user.id, message.message_id)
                    await message.answer(
                        "<b>Введите сумму для пополнения средств</b>",
                        reply_markup=all_back_to_main_default,
                    )
                else:
                    check_pass = True
            except json.decoder.JSONDecodeError:
                check_pass = True

            if check_pass:
                await message.answer("❗ Пополнение временно недоступно")
                await send_all_admin(
                    f"👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a> "
                    f"пытался пополнить баланс.\n"
                    f"<b>❌ QIWI кошелёк не работает. Срочно замените его.</b>"
                )
        else:
            await message.answer("❗ Пополнение временно недоступно")
            await send_all_admin(
                f"👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a> "
                f"пытался пополнить баланс.\n"
                f"<b>❌ QIWI кошелёк недоступен. Срочно замените его.</b>"
            )
    else:
        await message.answer("❗ Пополнения в боте временно отключены")


@dp.message_handler(text="💵 Оплата картой", state="*")
async def show_search(message: types.Message, state: FSMContext):
    check_pass = False
    get_payment = get_paymentx()
    if get_payment[5] == "True":
        if (
            get_payment[0] != "None"
            and get_payment[1] != "None"
            and get_payment[2] != "None"
        ):
            try:

                await bot.delete_message(message.from_user.id, message.message_id)
                await message.answer(
                    "<b>Введите сумму для пополнения средств</b>",
                    reply_markup=all_back_to_main_default,
                )
                await StorageQiwi.balance_input.set()
            except:
                print("ошибка")


@dp.message_handler(text="📋 Запланировать посещение", state="*")
async def show_s1earcsh(message: types.Message, state: FSMContext):
    # booking_park.json
    await message.answer(
        "Заполните форму ниже:\n✍ Напишите:\n1️⃣ Дата\n2️⃣ Время\n3️⃣ Ф.И.О.\n4️⃣ Количество человек\n5️⃣ Номер телефона"
    )
    await StorageQiwi.booking_prk.set()
    # 📔 Активности парка


@dp.message_handler(state=StorageQiwi.booking_prk)
async def schow_s1earcsh(message: types.Message, state: FSMContext):
    # check_len = message.text.split("\n")
    with open("booking_park.json", encoding="utf-8") as file:
        data_parse = json.load(file)

    if "Нет людей которые посетят парк" in data_parse:
        data_parse.remove("Нет людей которые посетят парк")
        data_parse.append(message.text)

        with open("booking_park.json", "w", encoding="utf-8") as f:
            json.dump(data_parse, f, indent=4, ensure_ascii=False)
        await message.answer("<b>Вы успешно добавлены в список</b>")

    else:
        data_parse.append(message.text)
        with open("booking_park.json", "w", encoding="utf-8") as f:
            json.dump(data_parse, f, indent=4, ensure_ascii=False)
        await message.answer("<b>Вы успешно добавлены в список</b>")

    await state.finish()


# 📃 Будущие посещения


@dp.message_handler(text="📃 Бронирования", state="*")
async def show_s1earcsh(message: types.Message, state: FSMContext):
    with open("booking_park.json", encoding="utf-8") as file:
        data1 = json.load(file)
    data = ""
    for i in data1:
        print(i)
        data += "".join(i) + "\n"

    salary_sales = f"Сегодня парк посетят:\n\n{data}"
    await bot.send_photo(
        message.from_user.id,
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgA0jj84K-yrYxBb6ZjMKstyD7pguFyxi6Gm6S9cKrxk0RJs7s6MITo1b5Xk5imQVFerk&usqp=CAU",
        caption=salary_sales,
    )


@dp.message_handler(text="📔 Активности парка", state="*")
async def show_searcsh(message: types.Message, state: FSMContext):
    with open("activities.json", encoding="utf-8") as f:
        data = json.load(f)

    print(data)
    await bot.send_photo(
        message.from_user.id,
        "https://www.finversia.ru/site/public/files/27/26393-932.jpg",
        data[0],
        reply_markup=activnost_kb,
    )


@dp.message_handler(state=StorageQiwi.balance_input)
async def process_name(message: types.Message, state: FSMContext):
    global PRICE
    PRICE = types.LabeledPrice(
        label="Пополнение баланса", amount=int(message.text) * 100
    )
    await state.finish()
    if (
        "1832575495:TEST:3867bc0eca33ad26a21b74ef80a572cd9f5dbd5805ce1613b810eb5ccd208bf4".split(
            ":"
        )[
            1
        ]
        == "TEST"
    ):
        await bot.send_message(message.chat.id, "pre_buy_demo_alert")
        await bot.send_invoice(
            message.chat.id,
            title="Пополнение",
            description="Пополнение баланса",
            provider_token="1832575495:TEST:3867bc0eca33ad26a21b74ef80a572cd9f5dbd5805ce1613b810eb5ccd208bf4",
            currency="rub",
            photo_url="",
            photo_height=0,  # !=0/None, иначе изображение не покажется
            photo_width=0,
            photo_size=0,
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[PRICE],
            start_parameter="time-machine-example",
            payload="some-invoice-payload-for-our-internal-use",
        )


@dp.message_handler(content_types=message.ContentTypes.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print("successful_payment:")
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f"{key} = {val}")

    await bot.send_message(
        message.chat.id,
        "successful_payment".format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency,
        ),
    )
    get_user = get_userx(user_id=message.chat.id)
    print([PRICE])
    update_userx(
        message.chat.id,
        balance=int(get_user[4]) +
        message.successful_payment.total_amount // 100,
    )

    await message.answer("Успешно выдан баланс")


# @dp.pre_checkout_query_handler(func=lambda query: True)
# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print("order_info")
    print(pre_checkout_query.order_info)

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(text="✏ Промокод", state="*")
async def gewt_chfdsdat_id3212(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите название промокода</b>")
    await StorageUsers.get_coupons_name_a.set()


# 📓 Контакты кинотеатра
@dp.message_handler(text="📓 Контакты кинотеатра", state="*")
async def gewt_chfsdsdat_id2(message: types.Message, state: FSMContext):
    salary_sales = """
<b>🎥Кинотеатр "КИНОСТАР"</b>
<b>Контактный телефон:</b> +7 (928) 017 20 22
Чеченская республика г. Грозный ТРЦ «ГРАНД ПАРК», 364060
Все вопросы, жалобы и предложения в DIRECT <b>@kinostar_95</b>


"""
    await bot.send_photo(
        message.from_user.id,
        "https://www.mos.ru/upload/newsfeed/newsfeed/GL(188851).jpg",
        caption=salary_sales,
        reply_markup=link_inst,
    )


@dp.message_handler(text="🔎 Меню", state="*")
async def gewtdat_id3212(message: types.Message, state: FSMContext):
    try:
        global id_user
        global get_items
        global items_list
        global items_dict
        id_user = str(message.from_user.id)
        get_items = get_all_positionsx()

        items_dict = {}
        items_list = []

        for i in get_items:
            items_dict[i[2]] = {"position_id": int(
                i[1]), "category_id": int(i[7])}

        for i in get_items:
            items_list.append(i[2])

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[id_user]["count_menu"])

        if count >= len(items_list):

            logger.warning(f"{len(items_list)} | {count} | {type(count)}")

            data[id_user] = {"count": "0", "count_menu": "0"}

            with open("count.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            await message.answer(
                'Меню закончилось, нажмите повторно кнопку "Меню", чтобы повторно посмотреть меню.'
            )

        else:

            global position_id
            global remover
            global category_id
            global get_position
            global get_category

            position_id = items_dict[items_list[count]]["position_id"]
            remover = 0
            category_id = items_dict[items_list[count]]["category_id"]

            get_position = get_positionx("*", position_id=position_id)
            get_category = get_categoryx("*", category_id=category_id)

            get_items = get_itemsx("*", position_id=position_id)

            send_msg = (
                f"<b>🎁 Покупка товара:</b>\n"
                f"\n"
                f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
                f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
                f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
                f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
                f"<b>📜 Описание:</b>\n"
                f"{get_position[4]}\n"
            )
            if len(get_position[5]) >= 5:
                await message.delete()

            else:
                await message.edit_text(
                    send_msg,
                    reply_markup=open_item_func(
                        position_id, remover, category_id),
                )

            data[id_user] = {"count": "0", "count_menu": str(count)}

            with open("count.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    except:
        with open("count.json", "r", encoding="utf-8") as file:
            x = json.load(file)

        x[id_user] = {"count": "0", "count_menu": "0"}

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(x, f, indent=4, ensure_ascii=False)

        for i in get_items:
            items_dict[i[2]] = {"position_id": int(
                i[1]), "category_id": int(i[7])}

        for i in get_items:
            items_list.append(i[2])

        with open("count.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        count = int(data[id_user]["count_menu"])

        if count >= len(items_list):

            logger.warning(f"{len(items_list)} | {count} | {type(count)}")

            data[id_user] = {"count": "0", "count_menu": "0"}

            with open("count.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            await message.answer(
                'Меню закончилось, нажмите повторно кнопку "Меню", чтобы повторно посмотреть меню.'
            )

        else:

            position_id = items_dict[items_list[count]]["position_id"]
            remover = 0
            category_id = items_dict[items_list[count]]["category_id"]

            get_position = get_positionx("*", position_id=position_id)
            get_category = get_categoryx("*", category_id=category_id)

            get_items = get_itemsx("*", position_id=position_id)

            send_msg = (
                f"<b>🎁 Покупка товара:</b>\n"
                f"\n"
                f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
                f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
                f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
                f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
                f"<b>📜 Описание:</b>\n"
                f"{get_position[4]}\n"
            )
            if len(get_position[5]) >= 5:
                await message.delete()
                await message.answer_photo(
                    get_position[5],
                    send_msg,
                    reply_markup=open_item_func(
                        position_id, remover, category_id),
                )
            else:
                await message.edit_text(
                    send_msg,
                    reply_markup=open_item_func(
                        position_id, remover, category_id),
                )

            data[id_user] = {"count": "0", "count_menu": str(count)}

            with open("count.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="next1", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    # await bot.delete_message(chat_id=id_user, message_id=call.message.message_id)

    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    logger.debug(id_user)
    logger.debug(id_user)
    count = data[id_user]["count_menu"]

    count = int(count)

    if 0 > count:
        count = 0
    else:
        pass

    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[id_user]["count_menu"])

    if count >= len(items_list):

        logger.warning(f"{len(items_list)} | {count} | {type(count)}")

        data[id_user] = {"count": "0", "count_menu": "0"}

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        await call.message.answer(
            'Меню закончилось, нажмите повторно кнопку "Меню", чтобы повторно посмотреть меню.'
        )

    else:

        position_id = items_dict[items_list[count]]["position_id"]
        remover = 0
        category_id = items_dict[items_list[count]]["category_id"]

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=open_item_func(
                    position_id, remover, category_id)
            )

        count += 1

        logger.success("Dumped")

        data[id_user] = {"count": "0", "count_menu": str(count)}

        with open("count.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_startswith="back1", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):

    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = data[id_user]["count_menu"]

    count = int(count)
    count += 1

    if 0 > count:
        count = 0
    else:
        pass

    get_items = get_all_positionsx()

    items_dict = {}
    items_list = []

    for i in get_items:
        items_dict[i[2]] = {"position_id": int(i[1]), "category_id": int(i[7])}

    for i in get_items:
        items_list.append(i[2])

    with open("count.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    count = int(data[id_user]["count_menu"])

    if count >= len(items_list):

        logger.warning(f"{len(items_list)} | {count} | {type(count)}")

        data[id_user] = {"count": "0", "count_menu": "0"}

        with open("count.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        await call.message.answer(
            'Меню закончилось, нажмите повторно кнопку "Меню", чтобы повторно посмотреть меню.'
        )

    else:

        position_id = items_dict[items_list[count]]["position_id"]
        remover = 0
        category_id = items_dict[items_list[count]]["category_id"]

        logger.warning(f"{count} | {type(count)}")

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)

        get_items = get_itemsx("*", position_id=position_id)

        send_msg = (
            f"<b>🎁 Покупка товара:</b>\n"
            f"\n"
            f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n"
            f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n"
            f"<b>💵 Стоимость:</b> <code>{get_position[3]} руб.</code>\n"
            f"<b>📦 Количество:</b> <code>{len(get_items)} шт.</code>\n"
            f"<b>📜 Описание:</b>\n"
            f"{get_position[4]}\n"
        )
        if len(get_position[5]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(
                get_position[5],
                send_msg,
                reply_markup=open_item_func(position_id, remover, category_id),
            )
        else:
            await call.message.edit_text(
                send_msg, reply_markup=open_item_func(
                    position_id, remover, category_id)
            )

    count -= 1

    logger.success("Dumped")

    data[id_user] = {"count": "0", "count_menu": str(count)}

    with open("count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 📽 Сейчас в кино


@dp.message_handler(text="📽 Сейчас в кино", state="*")
async def gewt_chfdsdat_id3212(message: types.Message, state: FSMContext):

    with open("kino.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        more = data[str(1)]["more"]
        await bot.send_photo(
            message.from_user.id,
            data[str(1)]["img_link"],
            caption=data[str(1)]["desc"],
            reply_markup=next_back_inl(more),
        )

    await StorageUsers.kinoteatr.set()


@dp.callback_query_handler(lambda c: c.data == "next", state=StorageUsers.kinoteatr)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    # try:
    id_count = str(callback_query.from_user.id)
    with open("count.json", "r", encoding="utf-8") as f:
        count = json.load(f)

    with open("kino.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if str(callback_query.from_user.id) in count:
        count = count[id_count]["count"]
    else:
        count[str(callback_query.from_user.id)] = {
            "count": "0", "count_menu": "0"}

        with open("count.json", "w") as file:
            json.dump(count, file, indent=4, ensure_ascii=False)

        count = 0
    count = int(count)
    count += 1

    if count >= len(data) + 1:
        count = 0

        more = data[str(1)]["more"]
        await bot.send_photo(
            callback_query.from_user.id,
            data[str(1)]["img_link"],
            caption=data[str(1)]["desc"],
            reply_markup=next_back_inl(more),
        )
    else:
        more = data[str(count)]["more"]
        await bot.send_photo(
            callback_query.from_user.id,
            data[str(count)]["img_link"],
            caption=data[str(count)]["desc"],
            reply_markup=next_back_inl(more),
        )

    with open("count.json", "r", encoding="utf-8") as f:
        counts = json.load(f)

    counts[id_count] = {"count": str(count), "count_menu": "0"}
    with open("count.json", "w") as file:
        json.dump(counts, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(lambda c: c.data == "back", state=StorageUsers.kinoteatr)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    # try:
    id_count = str(callback_query.from_user.id)
    with open("count.json", "r", encoding="utf-8") as f:
        count = json.load(f)

    with open("kino.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if str(callback_query.from_user.id) in count:
        count = count[id_count]["count"]
    else:
        count[callback_query.from_user.id] = {"count": "0", "count_menu": "0"}
        logger.success(count)
        with open("count.json", "w") as file:
            json.dump(count, file, indent=4, ensure_ascii=False)

        count = 0
    count = int(count)
    count -= 1

    if count >= len(data) + 1:
        count = 0
        logger.debug("Каунт больше чем дата")
        more = data[str(1)]["more"]
        await bot.send_photo(
            callback_query.from_user.id,
            data[str(1)]["img_link"],
            caption=data[str(1)]["desc"],
            reply_markup=next_back_inl(more),
        )
    else:
        if int(count) == 0:
            more = data[str(1)]["more"]
            await bot.send_photo(
                callback_query.from_user.id,
                data[str(1)]["img_link"],
                caption=data[str(1)]["desc"],
                reply_markup=next_back_inl(more),
            )
            count = 1
        else:
            logger.debug(count)
            more = data[str(count)]["more"]
            await bot.send_photo(
                callback_query.from_user.id,
                data[str(count)]["img_link"],
                caption=data[str(count)]["desc"],
                reply_markup=next_back_inl(more),
            )

    with open("count.json", "r", encoding="utf-8") as f:
        counts = json.load(f)

    counts[id_count] = {"count": str(count), "count_menu": "0"}
    with open("count.json", "w") as file:
        json.dump(counts, file, indent=4, ensure_ascii=False)


# 📒 Расписание


@dp.message_handler(text="📒 Расписание", state="*")
async def gewt_chfdsdat_id3212(message: types.Message, state: FSMContext):
    salary_sales = """
<b>График работы</b>с 10:00 до 22:00
<b>Контактный телефон:</b> +7 (928) 017 20 22


"""
    await bot.send_photo(
        message.from_user.id,
        "https://www.tsuab.ru/upload/iblock/433/Grafik-navchalnogo-protsesu.jpg",
        caption=salary_sales,
    )


@dp.message_handler(text="⬅️ На главную", state="*")
async def gewt_chfdszdat_id3212(message: types.Message, state: FSMContext):
    await message.answer(
        "Используйте кнопки управления", reply_markup=check_user_out_func(message.from_user.id)
    )
    await state.finish()


@dp.message_handler(text="🎦 Кинотеатр", state="*")
async def gewt_chfdsdat_id3212(message: types.Message, state: FSMContext):
    await message.answer("Используйте кнопки управления", reply_markup=kino_teatr)


@dp.message_handler(state=StorageUsers.get_coupons_name_a)
async def sget_chdat_id3212(message: types.Message, state: FSMContext):
    coupons_name = message.text
    with open("coupons.json") as file:
        data = json.load(file)

    for i in data:
        if coupons_name in i:
            # await message.answer("Купон найден")
            if str(message.from_user.id) in data[i]["tg_ids"]:
                await message.answer("<b>Промокод уже активирован</b>")
            else:

                data[i]["tg_ids"] += ", " + str(message.from_user.id)
                if 0 >= int(data[i]["count"]):
                    await message.answer("<b>Купоны закончились</b>")
                else:
                    data[i]["count"] = data[i]["count"] - 1
                    await message.answer("<b>Купон активирован</b>")
                    with open("coupons.json", "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)

                    get_user = get_userx(user_id=message.chat.id)
                    balance_coupons = data[i]["price"]

                    update_userx(
                        message.chat.id, balance=int(
                            get_user[4]) + balance_coupons
                    )

        else:
            await message.answer("<b>Такого промокода нет</b>")

    await state.finish()

    # @dp.message_handler(commands=['buy'])
    # async def process_buy_command(message: types.Message):
    #     if '401643678:TEST:4e9aad50-5060-441b-a1bd-5418a6d7ff5d'.split(':')[1] == 'TEST':
    #         await bot.send_message(message.chat.id, 'pre_buy_demo_alert')
    #         await bot.send_invoice(
    #             message.chat.id,
    #             title='Пополнение',
    #             description='Пополнение баланса.',
    #             provider_token='401643678:TEST:4e9aad50-5060-441b-a1bd-5418a6d7ff5d',
    #             currency='rub',
    #             photo_url='',
    #             photo_height=0,  # !=0/None, иначе изображение не покажется
    #             photo_width=0,
    #             photo_size=0,
    #             is_flexible=False,  # True если конечная цена зависит от способа доставки
    #             prices=[PRICE],
    #             start_parameter='time-machine-example',
    #             payload='some-invoice-payload-for-our-internal-use'
    #         )


@dp.message_handler(text="🍀 Благотворительность", state="*")
async def sgewt_chfdsdat_id3212(message: types.Message, state: FSMContext):
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
    <b>Благотворительный фонд Ахмат Кадырова</b>\n\tС каждой покупки 5% с суммы покупки идет на благотворительность\n\tСобрано денег в этом месяце: <b> {blagotvoritelnost} руб.</b>\n\n\nИнформация об фонде:\nАдрес: Чеченская Республика, г. Грозный, ул. 8-я Линия 10, 364017\n
График работы: с 14:00 до 18:00\n
Телефон: 8 (967) 948-16-14
"""

    await bot.send_photo(
        message.from_user.id,
        "https://sun9-80.userapi.com/impf/c622216/v622216019/277a1/CazADClEUsE.jpg?size=2560x1707&quality=96&sign=7d5eb7f867db487d5f2fceb10459e6ca&type=album",
        caption=salary_sales,
        reply_markup=faq_,
    )


# 🗺 Карта


@dp.message_handler(text="🗺 Карта", state="*")
async def sgewt_chfdssdat_id3212(message: types.Message, state: FSMContext):
    await message.answer_location(43.345857, 45.640887)


@dp.message_handler(text="🚕 Заказать Такси", state="*")
async def sgewt_chfdssdat_id3212(message: types.Message, state: FSMContext):
    salary_sales = f"""
    Заказать такси:
        YANDEX TAXI - https://clck.ru/ZSA96
        MAXIM TAXI -  https://clck.ru/ZSA9c
    """

    await bot.send_photo(
        message.from_user.id,
        "https://business-planner.ru/wp-content/uploads/2016/09/taksi.jpg",
        caption=salary_sales,
    )


# https://business-planner.ru/wp-content/uploads/2016/09/taksi.jpg
# 🚕 Заказать Такси


@dp.message_handler(commands=["test"])
async def cmd_image(message: types.Message):
    with open("images/menu.mp4", "rb") as video:
        await message.answer_video(video)
