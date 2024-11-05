from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class MoodTracking(Base):
    __tablename__ = "moods"
    id = Column(Integer, primary_key=True, index=True)
    mood_description = Column(String, index=True)
    mood = Column(String)