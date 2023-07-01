import json

from sqlalchemy.orm import Session

import src.user.models as models
from src.user.constants import CONV_HISTORY_LIMIT


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: int) -> models.User:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str) -> models.User:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_user_by_nickname(self, nickname: str) -> models.User:
        return self.db.query(models.User).filter(models.User.nickname == nickname).first()
    
    def create_user(self, user: models.User) -> models.User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_conv_history(
        self, 
        user: models.User, 
        filename: str
        ) -> models.User:
        conv_history_list: list[str] = json.loads(user.conv_history)
        conv_history_list.append(filename)
        if not user.premium and len(conv_history_list) > CONV_HISTORY_LIMIT:
            conv_history_list.pop(0)
        updated_conv_history = json.dumps(conv_history_list)
        user.conv_history = updated_conv_history
        self.db.commit()
        self.db.refresh(user)
        
        return user
