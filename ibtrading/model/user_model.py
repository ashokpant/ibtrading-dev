from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<UserModel(username={self.username}, full_name={self.full_name}, role={self.role})>"