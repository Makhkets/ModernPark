# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageUsers(StatesGroup):
    here_input_count_buy_item = State()
    here_cache_position_id = State()
    here_cache_count_item = State()
    activity = State()

    get_count_users_c = State()
    get_price_users_c = State()
    get_name_coupons_c = State()

    get_coupons_name_a = State()

    kinoteatr = State()

    bronirovanie = State()
    bronirovanie2 = State()
