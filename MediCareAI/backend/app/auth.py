from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from .config import settings
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
def hash_password(password:str)->str:return pwd_context.hash(password)
def verify_password(password:str,hashed:str)->bool:return pwd_context.verify(password,hashed)
def create_access_token(user_id:int)->str:return jwt.encode({'sub':str(user_id),'exp':datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_minutes)},settings.secret_key,algorithm='HS256')
def get_user_id_from_token(token:str)->int|None:
    try:return int(jwt.decode(token,settings.secret_key,algorithms=['HS256'])['sub'])
    except (JWTError,KeyError,TypeError,ValueError):return None
