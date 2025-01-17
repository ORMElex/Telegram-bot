import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand,  BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from openai import OpenAI
from data_base.dbwork import create_tables


BOT_TOKEN = config("TOKEN")
OpenAI_TOKEN = config("My_OpenAI_API_Key_2")

async def set_commands():
    commands = [
        BotCommand(command='start', description='старт'),
        BotCommand(command='help', description='помощь')
        ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    await create_tables()
    for admin in admins:
        try:
            await bot.send_message(admin, "Бот запустился")
        except:
            pass

async def stop_bot():
    for admin in admins:
        try:
            await bot.send_message(admin, "Бот отключился")
        except:
            pass

admins = [int(adm) for adm in config('ADMINS').split(',')]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token= BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
client = OpenAI(
    api_key=OpenAI_TOKEN,
    base_url="https://api.proxyapi.ru/openai/v1",
    )
dp = Dispatcher()
