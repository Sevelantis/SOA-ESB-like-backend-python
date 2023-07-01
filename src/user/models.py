'''models.py for db models'''

from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, default=None)
    nickname = Column(String(50), unique=True, index=True, default=None)
    auth_type = Column(String(20), default=None)
    premium = Column(Boolean, default=False)
    email_notification = Column(Boolean, default=True)
    whatsapp_notification = Column(Boolean, default=False)
    sms_notification = Column(Boolean, default=False)
    profile_picture = Column(String(256), default=None)
    conv_history = Column(Text(), default='[]')
