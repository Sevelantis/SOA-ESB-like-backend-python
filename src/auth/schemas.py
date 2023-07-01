from typing import Optional
from pydantic import BaseModel, EmailStr, validator

class SessionData(BaseModel):
    user_id: Optional[int]
    user_identification: Optional[str]
    auth_type: Optional[str]
