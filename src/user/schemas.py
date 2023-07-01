# A way to tell pydantic that the id field is optional.
from typing import Optional
from pydantic import BaseModel, validator, EmailStr


class User(BaseModel):
    email: EmailStr = ""
    nickname: Optional[str] = ""
    auth_type: str = ""
    premium: bool = False
    email_notification: bool = True
    whatsapp_notification: bool = False
    sms_notification: bool = False
    profile_picture: str = ""
    conv_history: Optional[list[str]] = []
    
    class Config:
        orm_mode = True
        
    # @classmethod
    # def from_orm(cls, user):
    #     data = user.__dict__.copy()
    #     conv_history_str = data.pop('conv_history')
    #     data['conv_history'] = conv_history_str.strip('[]').replace("'", "").split(", ")
    #     return cls(**data)

'''Create'''
class UserCreate(User):
    pass


'''Read'''
class UserRead(User):
    id: int
