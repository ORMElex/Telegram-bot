import asyncio
from Createbot import bot, dp, start_bot
from RouterHandler import router, admin_router, sub_router


async def main() -> None:
    await start_bot()
    dp.include_router(router=router)
    dp.include_router(router=sub_router)
    dp.include_router(router=admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())