from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import data_base.dbreq as dbr

class LastKB ():
    def __init__(self) -> None:
        self.last_keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Главное меню")]],
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Выберите режим работы"
        )

lastkb = LastKB()

def main_kb():
    kb_list = [
        [KeyboardButton(text="Диалог"), KeyboardButton(text="Тренировать слова")],
        [KeyboardButton(text="Тесты"), KeyboardButton(text="О боте")]
    ]
    lastkb.last_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите режим работы"
    )
    return lastkb.last_keyboard

def TrainWord_kb():
    kb_list=[
        [KeyboardButton(text="Учить новые слова"), KeyboardButton(text="Список слов")],
        [KeyboardButton(text="Добавить слова в список"), KeyboardButton(text="Удалить слово из списка")],
        [KeyboardButton(text="Главное меню")]
    ]
    lastkb.last_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите режим работы"
    )
    return lastkb.last_keyboard

def LearnWord_kb():
    kb_list=[
        [KeyboardButton(text="Да!")],
        [KeyboardButton(text="Главное меню")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите режим работы"
    )

def DeleteWord_kb():
    kb_list=[
        [KeyboardButton(text="Удалить конкретное слово из списка"), KeyboardButton(text="Удалить все слова из списка")],
        [KeyboardButton(text="Главное меню")]
    ]
    lastkb.last_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите режим работы"
    )
    return lastkb.last_keyboard
    
def Dialog_kb():
    last_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Главное меню")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return last_keyboard

def Start_kb():
    lastkb.last_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return lastkb.last_keyboard

def MainMenu_kb():
    last_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Главное меню")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return last_keyboard

async def ChnlToFollow_kb() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    chnl_list = await dbr.get_channel_to_subscribe()
    for channel in chnl_list:
        inline_kb.add(InlineKeyboardButton(text=channel.channel_label, url=channel.channel_url))
    inline_kb.add(InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription"))
    return inline_kb.adjust(1).as_markup()
