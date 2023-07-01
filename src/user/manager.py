import src.user.models as models
from src.auth.constants import CLASSICO, GITHUB, GOOGLE
from src.auth.utils import retrieve_auth_type
from src.user.factory import UserFactory
from src.user.repository import UserRepository

'''
use super_db;
show tables;
select * from users;
'''

class UserManager:
    def __init__(self, user_factory: UserFactory, user_repository: UserRepository) -> None:
        self.user_factory = user_factory
        self.user_repository = user_repository
    
    def process_user_auth(self, userinfo: dict) -> models.User:
        auth_type = retrieve_auth_type(userinfo['sub'])
        user: models.User = None
        if auth_type in [GOOGLE, CLASSICO]:
            user = self.user_repository.get_user_by_email(email=userinfo['email'])
        elif auth_type in [GITHUB]:
            user = self.user_repository.get_user_by_nickname(nickname=userinfo['nickname'])
        if not user:
            if auth_type == GITHUB:
                user = self.user_factory.create_github_user(userinfo=userinfo)
            elif auth_type == GOOGLE:
                user = self.user_factory.create_google_user(userinfo=userinfo)
            elif auth_type == CLASSICO:
                user = self.user_factory.create_classico_user(userinfo=userinfo)
                
        return user
