from datetime import datetime

import pytz
from sqlalchemy import BIGINT, TIMESTAMP, func, Column
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    chat_id: Mapped[int] = mapped_column(__type_pos=BIGINT)

