# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from data.config import admins


def check_user_out_func(user_id):
    menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_default.row("🔍 Меню")
    menu_default.row(
        "💰 Доплата наличными", "📱 Профиль", "🎁 Покупка", "💵 Пополнение баланса"
    )
    menu_default.row("✏ Промокод", "📓 Меню ресторана", "🎦 Кинотеатр")
    # menu_default.row("🗺 Карта", "🚕 Заказать Такси")
    menu_default.row(
        "📕 Поддержка", "📔 Активности парка", "ℹ FAQ", "🍀 Благотворительность"
    )
    menu_default.row("📋 Запланировать посещение", "📃 Бронирования")

    if str(user_id) in admins:
        menu_default.row("🎁 Управление товарами 🖍", "💸 Зарплата", "📰 Информация о боте")
        menu_default.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
    return menu_default


all_back_to_main_default = ReplyKeyboardMarkup(resize_keyboard=True)
all_back_to_main_default.row("⬅ На главную")
# ⬅️ На главную
