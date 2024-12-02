from datetime import datetime

from sqlalchemy import Column, BIGINT, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True)  # Primary key column
    chat_id = Column(BIGINT)
    login_code = Column(String)
    password = Column(String)
    token = Column(String)
    user_role = Column(String, default='user')
    received_date = Column(DateTime, default=datetime.now)  # Use default=datetime.now
