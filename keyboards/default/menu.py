# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import *
from aiogram.utils import *
from data.config import admins


def check_user_out_func(user_id):
    menu_default_main = ReplyKeyboardMarkup(resize_keyboard=True)

    menu_default_main.row("🏞 Парк", "💼 Активности парка")
    menu_default_main.row("🛠 Управление парком")
    if str(user_id) in admins:
        menu_default_main.row("🖥 Меню администратора")
    
    return menu_default_main

kb_park = ReplyKeyboardMarkup(resize_keyboard=True)
kb_park.row("🔍 Меню")
kb_park.row("📱 Профиль", "✏ Промокод", "🎁 Покупка")
kb_park.row("💵 Пополнение баланса", "💰 Доплата наличными")
kb_park.row("⬅ На главную")

active_park = ReplyKeyboardMarkup(resize_keyboard=True)
active_park.row("📕 Поддержка", "ℹ FAQ")
active_park.row("📔 Активности парка", "📃 Бронирования", "🍀 Благотворительность")
active_park.row("🎦 Кинотеатр")
active_park.row("⬅ На главную")

kb_park_func = ReplyKeyboardMarkup(resize_keyboard=True)
kb_park_func.row("📓 Меню ресторана")
# kb_park_func.row("🗺 Карта", "💻 Реклама", "🚕 Заказать Такси")
kb_park_func.row("🗺 Карта", "💻 Реклама")
kb_park_func.row("📋 Запланировать посещение")
kb_park_func.row("⬅ На главную")

admin_func_ = ReplyKeyboardMarkup(resize_keyboard=True)
admin_func_.row("🎁 Управление товарами 🖍")
admin_func_.row("💸 Зарплата", "📰 Информация о боте")
admin_func_.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
admin_func_.row("⬅ На главную")

all_back_to_main_default = ReplyKeyboardMarkup(resize_keyboard=True)
all_back_to_main_default.row("⬅ На главную")

reklama = InlineKeyboardMarkup()
reklama.row(InlineKeyboardButton('Оплатить рекламу с баланса', callback_data='reklama_oplata'))

podverjdenie = InlineKeyboardMarkup()
podverjdenie.row(InlineKeyboardButton('✅ Подтвердить', callback_data='podverdits'), InlineKeyboardButton('❌ Отказать', callback_data='otkazat'))