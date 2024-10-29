from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base


sqlite_database = 'sqlite:///users&qs.db'
engine = create_engine(sqlite_database, echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id  = Column(Integer, primary_key=True)
    tg_id = Column(String)
