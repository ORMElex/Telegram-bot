import random
from aiogram.enums import ContentType, ChatMemberStatus
from aiogram.types import Message
from Createbot import bot, logger
from data_base.dbreq import get_channel_to_subscribe, set_channel_to_subscribe, get_random_word_by_user_id_and_word_lvl

async def check_follow_on_chnl(tg_id: int) -> bool:
    try:
        channels = await get_channel_to_subscribe()
        if channels:
            for channel in channels:
                chat_name = channel.channel_url.split("/")[-1]
                member = await bot.get_chat_member(chat_id=f"@{chat_name}", user_id=tg_id)

                if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                    continue
                else:
                    return False
            
        return True
    except Exception as e:
        logger.error(f"Error: Utils: Something went wrong on checking a follow of a {tg_id} on the channel @{chat_name} /// {e}")
        return False
    

async def set_channels_to_sub(channel_url: str, channel_label:str):
    try:
        operation_result = await set_channel_to_subscribe(channel_url=channel_url, channel_label=channel_label)
        if operation_result:
            return f"Канал {channel_url}был добавлен в базу данных"
    except Exception as e:
        logger.error(f"Error: Utils: Something went wrong while adding a channel {channel_url} /// {e}")
        return  f"Канал {channel_url} не был добавлен в базу данных"


async def RandomLearningWord (mode: int, message: Message, words: list):
    try:
        while(True):
            lvl = random.randrange(1,5)
            words = await get_random_word_by_user_id_and_word_lvl(tg_id=message.from_user.id, lvl=lvl)
            if words:
                return words
    except Exception as e:
        logger.error(f"Error: Utils: Something went wrong while choosing random words /// {e}")
        return None