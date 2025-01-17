from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

Base = declarative_base()

class User(AsyncAttrs, Base):
    __tablename__='users'

    id = Column(Integer, nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    tg_id: Mapped[int] = mapped_column()
    words = relationship('Word', back_populates='user')
    context = relationship('DialogContext', back_populates='userc')

    def __repr__(self):
        return f"<User(id={self.id})>"

class Word(AsyncAttrs, Base):
    __tablename__='words'

    id = Column(Integer, nullable=False, primary_key=True)
    word:Mapped[str] = mapped_column(String)
    user_id = Column(Integer, ForeignKey('users.tg_id'), nullable=False)
    lvl: Mapped[int] = mapped_column(Integer)

    user = relationship('User', back_populates='words')

    def __repr__(self):
        return f"<Word (id={self.id}, User(id={self.user_id})>"
    
class DialogContext(AsyncAttrs, Base):
    __tablename__ = 'dialoguecontext'

    id = Column(Integer, nullable=False, primary_key=True)
    context: Mapped[str] = mapped_column(String)
    user_id = Column(Integer, ForeignKey('users.tg_id'), nullable=False)

    userc = relationship('User', back_populates='context')

    def __repr__(self):
        return f"<Context (id={self.id}, User(id={self.user_id}))"

class ChannelToSubscribe (AsyncAttrs, Base):
    __tablename__ = 'channels_to_sub'

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    channel_url: Mapped [str] = mapped_column(String)
    channel_label: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Channels (if={self.id})"