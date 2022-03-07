# - *- coding: utf- 8 - *-
from os import link
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки при поиске профиля через админ-меню
open_profile_inl = InlineKeyboardMarkup()
mybuy_kb = InlineKeyboardButton(text="🛒 Мои покупки", callback_data="my_buy")
mybuy_bkb = InlineKeyboardButton(text="💳 Бонусная карта", callback_data="bonus_card")
chat_link_bk = InlineKeyboardButton(text="👥 Чат", url="https://t.me/+o_lzftmG2PRhNzUy")
# open_profile_inl.add(input_kb, mybuy_kb, input_kb1)
open_profile_inl.row(mybuy_kb, chat_link_bk)
open_profile_inl.row(mybuy_bkb)

# Кнопка с возвратом к профилю
to_profile_inl = InlineKeyboardMarkup()
to_profile_inl.row(InlineKeyboardButton(text="📱 Профиль", callback_data="user_profile"))


def next_back_inl(uri):
    back_inline = InlineKeyboardButton("Назад", callback_data="back")
    next_inline = InlineKeyboardButton("Вперед", callback_data="next")
    yri = InlineKeyboardButton("🎬 Подробнее об фильме", url=uri)

    next_back_inline = InlineKeyboardMarkup().row(yri).row(back_inline, next_inline)
    return next_back_inline


# back_inline1 = InlineKeyboardButton('Назад', callback_data='back')
# next_inline1 = InlineKeyboardButton('Вперед', callback_data='next')
# next_back_inline1 = InlineKeyboardMarkup().row(back_inline1, next_inline1)

# next_back_inline1 = InlineKeyboardMarkup().row(back_inline1, next_inline1)

activnost = InlineKeyboardButton(
    "📱 Подробнее об активностях", url="https://www.instagram.com/park.kadyrova/"
)

activnost_kb = InlineKeyboardMarkup().row(activnost)


menu_category = InlineKeyboardMarkup()
# _1 = InlineKeyboardButton('🎫 Билеты', callback_data='ticket_menu')
_2 = InlineKeyboardButton("🍔 Бургеры, пиццы, стейки", callback_data="burger_menu")
_3 = InlineKeyboardButton("📙 Национальная кухня", callback_data="pizza_menu")
_4 = InlineKeyboardButton(
    "🍣 Суши и роллы, блюдо из морепродуктов", callback_data="sushi_menu"
)
_5 = InlineKeyboardButton(
    "👶🏻 Детское питание, мороженое, напитки", callback_data="napitki_menu"
)
_6 = InlineKeyboardButton(
    "📕 Заказать доставку",
    url="http://restaurant-benefis.ru/",
)

# menu_category.row(_1)
menu_category.row(_2, _3)
menu_category.row(_4, _5)
menu_category.row(_6)


menu_category_ = InlineKeyboardMarkup()
__2 = InlineKeyboardButton("🌐 Наш сайт", url="https://appreal.org/chechnya-15-object/")
__3 = InlineKeyboardButton(
    "📱 instagram", url="https://www.instagram.com/park.kadyrova/"
)
__4 = InlineKeyboardButton(
    "🗺 Карта",
    url="https://www.google.com/maps/place/%D0%9F%D0%B0%D1%80%D0%BA+%D0%9D%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9+%D0%9A%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D1%8B+%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8+%D0%9A%D0%B0%D0%B4%D1%8B%D1%80%D0%BE%D0%B2%D0%B0+%D0%90.%D0%90./@43.3491509,45.6415858,17z/data=!4m5!3m4!1s0x4051d21e966ede61:0x7475fa380e4ea9ad!8m2!3d43.3488388!4d45.6428947?hl=ru",
)


menu_category_.row(__2, __3)
menu_category_.row(__4)

faq_ = InlineKeyboardMarkup()
faq2 = InlineKeyboardButton(
    "📱 Instagram", url="https://www.instagram.com/fond_kadyrova/"
)

faq_.row(faq2)


link_inst = InlineKeyboardMarkup()
linst = InlineKeyboardButton("🌐 Сайт", url="https://kinostar3d.ru/gzn/")

link_inst.row(linst)
