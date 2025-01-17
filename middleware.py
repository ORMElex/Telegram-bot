from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from utils import check_follow_on_chnl
from Createbot import admins
import Keyboard as kb
import data_base.dbreq as dbr


class StarterMiddleware (BaseMiddleware):
    async def __call__(self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ):
        return await handler(event, data)

class IsSubscribedonChannel (StarterMiddleware):
    async def __call__(self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ):
        if event.from_user.id in admins:
            result = await handler(event, data)
            print("admin")
            return result
        else:
            if await check_follow_on_chnl(tg_id=event.from_user.id):
                result = await handler(event, data)
                return result
            else:
                print("Не подписан")
                await event.answer("Чтобы пользоваться ботов нужно подписаться на канал:", reply_markup=await kb.ChnlToFollow_kb())
                

class IsAdmin (StarterMiddleware):
    async def __call__(self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        if event.from_user.id in admins:
            result = await handler(event, data)
            print("admin")
            return result
        else:
            print("Доступ запрещён")
            await event.answer("Доступ запрещён!")

