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




Sessionlocal = sessionmaker(autoflush=False, bind=engine)

async def add_user(tg_id, username=None):
    db = Sessionlocal()
    try:
        user = db.query(User).filter(User.tg_id == tg_id).first()
        if not user:
            new_user = User(tg_id=tg_id, username=username)
            db.add(new_user)
            db.commit()
            return new_user
        return user
    finally:
        db.close()

async def new_question(tg_id, question_text):
    db = Sessionlocal()
    try:
        user = db.query(User).filter(User.tg_id == tg_id).first()
        if user:
            question = Question(user_id=user.id, question_text=question_text)
            db.add(question)
            db.commit()
            return question
        else:
            raise ValueError("Пользователь не найден.")
    finally:
        db.close()

async def add_answer(tg_id, question_id, answer_text):
    db = Sessionlocal()
    try:
        user = db.query(User).filter(User.tg_id == tg_id).first()
        question = db.query(Question).filter(Question.id == question_id).first()
        
        if user and question:
            answer = Answer(question_id=question.id, user_id=user.id, answer_text=answer_text)
            db.add(answer)
            db.commit()
            return answer
        else:
            raise ValueError("Пользователь или вопрос не найден.")
    finally:
        db.close()


