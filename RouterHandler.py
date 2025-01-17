from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import OpenAIwork
import Keyboard as kb
import data_base.dbreq as dbr
from Createbot import logger
import utils as u
from utils import check_follow_on_chnl
from middleware import IsSubscribedonChannel, IsAdmin, StarterMiddleware


BotVersion = "v. 0.0.1"
HELP = """List of availaible command:
- /start
- /help 
- /balance
"""
routerError = "Что-то пошло не так. Перезапустите, пожалуйста, бота"

class BotMode(StatesGroup):
    S_dialog = State()
    S_menu = State()
    S_trainwords = State()
    S_addword = State()
    S_addword2 = State()
    S_learnword = State()
    S_learnword2 = State()
    S_deleteword = State()

router = Router()
admin_router = Router()
sub_router = Router()

router.callback_query.outer_middleware(StarterMiddleware())
router.message.outer_middleware(StarterMiddleware())
admin_router.message.outer_middleware(IsAdmin())
sub_router.message.outer_middleware(IsSubscribedonChannel())


@router.message (Command(commands=["start","restart"]))
async def StartFunc (message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в  личный помощник с изучением иностранных языков.\nЗдесь вы можете изучить новые слова, попрактиковаться с чатом GPT в диалоге, изучить с ним новые для вас темы и проверить свои знания в тестах\nНажмите начать для продолжения", reply_markup=kb.Start_kb())
    await dbr.set_user(message.from_user.id, message.from_user.first_name)
    await dbr.delete_context(message.from_user.id)
    await state.set_state(BotMode.S_menu)

@router.message(F.text.in_({"Начать", "Главное меню"}))
async def MainMenu (message: Message, state: FSMContext):
    await state.set_state(BotMode.S_menu)
    await dbr.delete_context(message.from_user.id)
    await message.answer("Чем хотите заняться?", reply_markup=kb.main_kb())

@router.message(BotMode.S_menu)
async def MainMenuHandler(message: Message):
    await message.answer("Я не понимаю этой команды, прости!\n\nВыбери команду на клавиатуре:", reply_markup=kb.main_kb())

@router.message(Command("help"))
async def HelpCommand(message: Message):
    await message.answer(HELP, reply_markup=kb.MainMenu_kb())

@admin_router.message(Command("balance")) #("balance_id_387948964"))
async def BalanceCommand(message: Message):
    print(OpenAIwork.CheckBalanceProxiAPI())


@router.message(F.text == "Диалог")
async def StartDialog(message: Message, state: FSMContext):
    await state.set_state(BotMode.S_dialog)
    await message.answer("Здесь вы можете потренироваться в общении с чатом. Выберите/предложите тему для диалога или просто напишите hi", reply_markup=kb.Dialog_kb())

@sub_router.message(BotMode.S_dialog)
async def RequestToAI(message: Message, state:FSMContext):
    try:
        msg = await OpenAIwork.CreateMessagesForAI(messagefromuser=message.text, tg_id=message.from_user.id)
        completion = await OpenAIwork.CreateRequestToAI(msg)
        await message.answer(f"{completion.choices[0].message.content} + {completion.usage.completion_tokens} + {completion.usage.prompt_tokens}", reply_markup=kb.Dialog_kb())
        await dbr.add_context(tg_id=message.from_user.id, s_context=[f"user:{message.text}", f"assistant:{completion.choices[0].message.content}"])
    except Exception as e:
        await message.answer(f"Nice try! /// {e}")

@admin_router.message(F.text == "История диалога")
async def HistoryOfDialog(message: Message, state: FSMContext):
    try: 
        list = await OpenAIwork.CreateMessagesForAI(message.text, message.from_user.id)
        print(list)
        await message.answer("Отправил", reply_markup=kb.Dialog_kb())
    except TypeError:
        await message.answer("Nice try!")



@router.message(F.text == "Тренировать слова")
async def TrainWordFirst(message: Message, state: FSMContext):
    await state.set_state(BotMode.S_trainwords)
    await message.answer("Выберите режим работы", reply_markup=kb.TrainWord_kb())

@router.message(F.text =="Учить новые слова")
async def LearnWordsMode(message: Message, state:FSMContext):
    await message.answer("Готовы приступить?",reply_markup=kb.LearnWord_kb())
    await state.set_state(BotMode.S_learnword)

@router.message(F.text =="Список слов")
async def ListOfWordsMode(message: Message, state:FSMContext):
    words = await dbr.get_words_by_user_id(message.from_user.id)
    if not words:
        await message.answer("Список слов пуст", reply_markup=kb.TrainWord_kb())
    else:
        wordlist = "Вот ваш список слов\n"
        for word in words:
            wordlist += word.word
            wordlist += "\n"
        await message.answer(wordlist, reply_markup=kb.TrainWord_kb())

@router.message(F.text =="Добавить слова в список")
async def AddWordMode(message: Message, state:FSMContext):
    await state.set_state(BotMode.S_addword)
    await message.answer("Введите слово или список слов, которые хотите выучить")

@router.message(F.text =="Удалить слово из списка")
async def DeleteWordMode(message: Message, state: FSMContext):
    await message.answer("Введите режим удаления слова", reply_markup=kb.DeleteWord_kb())

@router.message(F.text =="Удалить конкретное слово из списка")
async def DeleteSpecificWordMode(message: Message, state: FSMContext):
    await state.set_state(BotMode.S_deleteword)
    await message.answer("Введите слово, которое хотите удалить")

@router.message(F.text =="Удалить все слова из списка")
async def DeleteAllWords(message: Message, state: FSMContext):
    await dbr.delete_all_word(message.from_user.id)
    await message.answer("Все слова были успешно удалены", reply_markup=kb.TrainWord_kb())

@sub_router.message(BotMode.S_learnword)
async def LearnWords (message: Message, state: FSMContext):
    try:
        await message.answer("В")
        words = await u.RandomLearningWord(message=message)
        
    except: 
        await message.answer(routerError, reply_markup=kb.TrainWord_kb())

@sub_router.message(BotMode.S_addword)
async def AddWords (message: Message, state: FSMContext):
    try:
        await dbr.set_word(tg_id=message.from_user.id, s_word=message.text)
        await message.answer("Слово было успешно добавлено", reply_markup=kb.TrainWord_kb())
        print(repr(message.text))
    except:
        await message.answer(routerError, reply_markup=kb.TrainWord_kb())

@sub_router.message(BotMode.S_deleteword)
async def DeleteWords (message: Message, state: FSMContext):
    try:
        await dbr.delete_word(tg_id=message.from_user.id, s_word=message.text)
        await message.answer("Слово было успешно удалено", reply_markup=kb.TrainWord_kb())
    except:
        await message.answer(routerError, reply_markup=kb.TrainWord_kb())




@router.callback_query(F.data == "check_subscription")
async def Check_Sub(callback : CallbackQuery):
    try:
        if await check_follow_on_chnl(tg_id=callback.from_user.id):
            await callback.answer()
            await callback.message.answer("Вы подписаны! Можете продолжать пользоваться ботом!", reply_markup=kb.lastkb.last_keyboard)
        else:
            await callback.answer()
            await callback.message.answer("Вы ещё не подпиcаны на каналы:", reply_markup=await kb.ChnlToFollow_kb())
    except Exception as e:
        logger.info(f"Error occured while checking follow on channels /// {e}")
        await callback.message.answer(routerError, reply_markup=kb.Start_kb())




@admin_router.message(Command("set_channel"))
async def SetChannelsToSubscribe(message: Message):
    operation_res = await dbr.set_channel_to_subscribe(channel_url = message.text.split(" ", 2)[1], channel_label=message.text.split(" ", 2)[2])
    await message.answer(operation_res)

    #await message.answer(message.text + "\n" + message.text.split(" ")[0])

@admin_router.message(Command("get_channels"))
async def GetChannelsToSubscribe(message: Message):
    channels = await dbr.get_channel_to_subscribe()
    msg = ""
    for chnl in channels:
        msg += chnl.channel_label
        msg += ": "
        msg += chnl.channel_url
        msg += "\n"
    await message.answer(msg)

@admin_router.message(Command("delete_channel"))
async def GetChannelsToSubscribe(message: Message):
    await dbr.delete_channel_to_subscribe(channel_url=message.text.split(" ", 1)[1])
    await message.answer("Канал удалён из списка")