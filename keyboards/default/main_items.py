# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

items_default = ReplyKeyboardMarkup(resize_keyboard=True)
items_default.add("📢 Добавить 2 свободных мест для бронирования")
# items_default.row("🎫 Карусель", "🎫 Колесо обозрения", "🎫 Комната смеха")
items_default.row("🎁 Добавить товары ➕", "🎁 Изменить товары 🖍", "🎁 Удалить товары ❌")
items_default.row("📁 Создать позицию ➕", "📁 Изменить позицию 🖍", "📁 Удалить позиции ❌")
items_default.row(
    "📜 Создать категорию ➕", "📜 Изменить категорию 🖍", "📜 Удалить категории ❌"
)
items_default.row("⬅ На главную")

skip_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
skip_send_image_default.row("📸 Пропустить")

cancel_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_send_image_default.row("📸 Отменить")

finish_load_items_default = ReplyKeyboardMarkup(resize_keyboard=True)
finish_load_items_default.row("📥 Закончить загрузку товаров")

oplata_s = ReplyKeyboardMarkup(resize_keyboard=True)
oplata_s.row("💵 Оплата киви", "💵 Оплата картой")
oplata_s.row("⬅ На главную")


kino_teatr = ReplyKeyboardMarkup(resize_keyboard=True)
kino_teatr.row("📒 Расписание", "📓 Контакты кинотеатра", "📽 Сейчас в кино")
kino_teatr.row("⬅️ На главную")

kino_teatr2 = ReplyKeyboardMarkup(resize_keyboard=True)
kino_teatr2.row("1", "2", "3", "4", "5")
kino_teatr2.row("⬅️ На главную")

#########################################################################
