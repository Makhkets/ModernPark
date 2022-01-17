# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageQiwi(StatesGroup):
    here_input_qiwi_secret = State()
    here_input_qiwi_login = State()
    here_input_qiwi_token = State()
    here_input_qiwi_amount = State()
    balance_input_minus = State()
    balance_input = State()
    balance_input_qiwi = State()
    booking_prk = State()
