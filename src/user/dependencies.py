'''dependencies.py - Dependency Injection for router.py'''

from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import src.user.models as models
from src.auth.dependencies import session_data
from src.auth.schemas import SessionData
from src.database.dependencies import database
from src.user.factory import UserFactory
from src.user.manager import UserManager
from src.user.repository import UserRepository


def user_repository(database: Session = Depends(database)) -> UserRepository:
    return UserRepository(db=database)

def user_factory(user_repository: UserRepository = Depends(user_repository)) -> UserFactory:
    return UserFactory(user_repository=user_repository)

def user_manager(
    user_factory: UserFactory = Depends(user_factory),
    user_repository: UserRepository = Depends(user_repository)
    ) -> UserManager:
    
    return UserManager(user_factory=user_factory, user_repository=user_repository)

def current_user(
    session_data: SessionData = Depends(session_data),
    user_repository: UserRepository = Depends(user_repository)
    ) -> models.User:
    if user := user_repository.get_user(user_id=session_data.user_id):
        return user
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Unprocessable entity.",
        )
