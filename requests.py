from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


sqlite_database = 'sqlite:///users&qs.db'
engine = create_engine(sqlite_database, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id  = Column(Integer, primary_key=True)
    tg_id = Column(String, nullable=False)
    username = Column(String, nullable=True)

    questions = relationship('Question', back_populates='user')
    answers = relationship('Answer', back_populates='user')



class Question(Base):
    __tablename__ = 'questions'

    id  = Column(Integer, primary_key=True)
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