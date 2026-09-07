from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from passlib.context import CryptContext
from .config import settings
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); ALGO='HS256'
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(sub): return jwt.encode({'sub':str(sub),'exp':datetime.now(timezone.utc)+timedelta(hours=24)},settings.secret_key,algorithm=ALGO)
def get_user_id(token):
    try: return int(jwt.decode(token,settings.secret_key,algorithms=[ALGO])['sub'])
    except (JWTError,KeyError,ValueError,TypeError): return None
