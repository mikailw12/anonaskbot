from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

sqlite_database = 'sqlite+aiosqlite:///users&qs.db'  # Измените на асинхронный драйвер
engine = create_async_engine(sqlite_database, echo=True)  # Используйте асинхронный движок
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(String, nullable=False)
    username = Column(String, nullable=True)

    questions = relationship('Question', back_populates='user')
    answers = relationship('Answer', back_populates='user')

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_text = Column(Text, nullable=False)

    user = relationship('User', back_populates='questions')
    answers = relationship('Answer', back_populates='question')

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answer_text = Column(Text, nullable=False)

    user = relationship('User', back_populates='answers')
    question = relationship('Question', back_populates='answers')

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user(tg_id):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:  # Используйте AsyncSession
        user = await session.execute(User.select().where(User.tg_id == tg_id))
        user = user.scalars().first()
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()
