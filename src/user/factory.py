
from src.auth.constants import GITHUB, GOOGLE, CLASSICO
import src.user.models as models
import src.user.schemas as schemas
from src.user.repository import UserRepository

class UserFactory:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def create_github_user(self, userinfo: dict) -> models.User:
        user = models.User(
            email=None,
            nickname=userinfo['nickname'],
            auth_type=GITHUB,
            premium=False,
            email_notification=True,
            whatsapp_notification=False,
            sms_notification=False,
            profile_picture=userinfo['picture'],
            conv_history='[]')
        
        return self.user_repository.create_user(user=user)
    
    def create_google_user(self, userinfo: dict) -> models.User:
        user = models.User(
            email=userinfo['email'],
            nickname=None,
            auth_type=GOOGLE,
            premium=False,
            email_notification=True,
            whatsapp_notification=False,
            sms_notification=False,
            profile_picture=userinfo['picture'],
            conv_history='[]')
        
        return self.user_repository.create_user(user=user)
    
    def create_classico_user(self, userinfo: dict) -> models.User:
        user = models.User(
            email=userinfo['email'],
            nickname=None,
            auth_type=CLASSICO,
            premium=False,
            email_notification=True,
            whatsapp_notification=False,
            sms_notification=False,
            profile_picture=userinfo['picture'],
            conv_history='[]')
        
        return self.user_repository.create_user(user=user)
    