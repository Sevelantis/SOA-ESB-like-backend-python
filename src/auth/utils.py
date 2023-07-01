'''utils.py - non-business logic functions, e.g. response normalization, data enrichment, etc.'''


from src.auth.constants import CLASSICO, GOOGLE, GITHUB
import src.config as config
import src.user.models as models
from src.auth.schemas import SessionData
from jose import jwt

def encoded_value(value):
    return jwt.encode(value, config.APP_SECRET_KEY)

def decoded_value(value):
    return jwt.decode(value, config.APP_SECRET_KEY)
    
def retrieve_auth_type(sub: str) -> str:
    if GOOGLE.lower() in sub.lower():
        return GOOGLE.lower()
    elif GITHUB.lower() in sub.lower():
        return GITHUB.lower()
    elif CLASSICO.lower() in sub.lower():
        return CLASSICO
    return CLASSICO
