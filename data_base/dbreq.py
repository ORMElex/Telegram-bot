from Createbot import logger
from .dbwork import connection
from .dbmodels import User, Word, DialogContext, ChannelToSubscribe
from sqlalchemy import select, delete
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

@connection
async def set_user(session, tg_id: int, username: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()
            logger.info(f"User with ID {tg_id} has beeb added")
            return None
        else:
            logger.info(f"User with ID {tg_id} has been found")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Error occured while adding new user: {e}")
        await session.rollback()

@connection
async def set_word(session, tg_id:int, s_word: str) -> Optional[Word]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else:
            words = s_word.split("\n")
            for wrd in words:
                word = await session.scalar(select(Word).filter_by(word=wrd))
                if not word:
                    new_word = session.add(Word(user_id=tg_id, word=wrd))
                    await session.commit()
                    logger.info(f"New word {s_word} of user with ID {tg_id} has been added")
                    return new_word
                else:
                    logger.info(f"This word {s_word} of user with ID {tg_id} is already added")
                    return word
    except SQLAlchemyError as e:
        logger.error(f"Error occured while adding new word {s_word}")
        await session.rollback()

@connection
async def get_words_by_user_id (session, tg_id:int):
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            #result = await session.execute(select(Word).filter_by(user_id=tg_id).all())
            #words = result.scalars().all
            result = await session.execute(select(Word).filter_by(user_id=tg_id))
            words = result.scalars().all()
            if not words:
                logger.info(f"List of words of user {tg_id} hasn't been found")
                return []
            else:
                logger.info(f"List of words of user {tg_id} has been found")
                return words
    except SQLAlchemyError as e:
        logger.error(f"Error occured while gettin list of words of user {tg_id}")
        return []
    
@connection
async def get_random_word_by_user_id_and_word_lvl (session, tg_id:int, lvl:int):
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            result = await session.execute(select(Word).filter((Word.user_id==tg_id) & (Word.lvl == lvl)))
            words = result.scalars().all()
            if not words:
                logger.info(f"List of words with lvl {lvl} of user {tg_id} hasn't been found")
                return []
            else:
                logger.info(f"List of words with lvl {lvl} of user {tg_id} has been found")
                return words
    except SQLAlchemyError as e:
        logger.error(f"Error occured while gettin list of words with lvl {lvl} of user {tg_id}")
        return []

@connection
async def delete_word(session, tg_id:int, s_word:str) -> Optional[Word]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            word = await session.scalar(select(Word).filter_by(word=s_word))
            if not word:
                logger.info(f"Word {s_word} of user with ID {tg_id} hasn't been found")
                return None
            else:
                await session.delete(word)
                await session.commit()
                logger.info(f"Word {s_word} of user with ID {tg_id} has been deleted")
                return word
    except SQLAlchemyError as e:
        logger.error(f"Error occured while deleting word {s_word}")
        await session.rollback()

@connection
async def delete_all_word(session, tg_id:int) -> Optional[Word]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            result = await session.execute(select(Word).filter_by(user_id=tg_id))
            words = result.scalars().all()
            if not words:
                logger.info(f"Words of user with ID {tg_id} hasn't been found")
                return None
            else:
                await session.execute(delete(Word).where(Word.user_id==tg_id))
                await session.commit()
                logger.info(f"Words of user with ID {tg_id} has been deleted")
                return words
    except SQLAlchemyError as e:
        logger.error(f"Error occured while deleting words")
        await session.rollback()

@connection
async def add_context(session, tg_id:int, s_context:list) -> Optional[list]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return "f"
        else:
            for cntxt in s_context:
                new_content = session.add(DialogContext(user_id = tg_id, context=cntxt))
            await session.commit()
            logger.info(f"New context {s_context} for user with ID {tg_id} has been added")
            return new_content
    except SQLAlchemyError as e:
        logger.error(f"Error occured while adding new context {s_context} /// {e}")
        await session.rollback()

@connection
async def get_context_by_user_id (session, tg_id:int) -> Optional[list]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            result = await session.execute(select(DialogContext).filter_by(user_id=tg_id))
            context = result.scalars().all()
            if not context:
                logger.info(f"List of context for user {tg_id} hasn't been found")
                return []
            else:
                logger.info(f"List of context for user {tg_id} has been found")
                return context
    except SQLAlchemyError as e:
        logger.error(f"Error occured while gettin context of user {tg_id} /// {e}")
        return []
    
@connection
async def delete_context(session, tg_id:int) -> Optional[Word]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))
        if not user:
            logger.info(f"User with ID {tg_id} hasn't been found")
            return None
        else: 
            #result = await session.execute(select(DialogContext).filter_by(user_id=tg_id))
            #context = result.scalar().all()
            context = await session.scalars(select(DialogContext).filter_by(user_id=tg_id))
            if not context:
                logger.info(f"Context of user with ID {tg_id} hasn't been found")
                return None
            else:
                await session.execute(delete(DialogContext).where(DialogContext.user_id==tg_id))
                await session.commit()
                logger.info(f"Context of user with ID {tg_id} has been deleted")
                return context
    except SQLAlchemyError as e:
        logger.error(f"Error occured while deleting context")
        await session.rollback()





@connection
async def get_channel_to_subscribe(session) -> Optional[list]:
    try:
        result = await session.execute(select(ChannelToSubscribe))
        channels = result.scalars().all()
        if channels:
            logger.info(f"List of channels has been found")
            return channels
        else:
            logger.info(f"List of channels hasn't been found")
            return None
    except SQLAlchemyError as e:
        logger.error(f"Error occured while getting list of channels to subscribe /// {e}")
        await session.rollback()


@connection
async def set_channel_to_subscribe(session, channel_url:str, channel_label:str) -> bool:
    try:
        session.add(ChannelToSubscribe(channel_url = channel_url, channel_label=channel_label))
        await session.commit()
        logger.info(f"Channel {channel_url} has been added")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error occured while setting list of channels to subscribe /// {e}")
        await session.rollback()
        return False
    
@connection
async def delete_channel_to_subscribe(session, channel_url:str) -> bool:
    try:
        channel = await session.scalar(select(ChannelToSubscribe).filter_by(channel_url=channel_url))
        if channel:
            await session.execute(delete(ChannelToSubscribe).where(ChannelToSubscribe.channel_url == channel_url))
            await session.commit()
            logger.info(f"Channel {channel_url} has been deleted")
            return channel
        else:
            logger.info(f"Channel {channel_url} hasn't been found")
            return None
        
    except SQLAlchemyError as e:
        logger.error(f"Error occured while deleting channel to subscribe /// {e}")
        await session.rollback()
