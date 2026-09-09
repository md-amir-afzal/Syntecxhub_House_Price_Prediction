from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"


def hash_password(password: str) -> str:
    return pwd.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)


def create_token(sub: int) -> str:
    return jwt.encode(
        {"sub": str(sub), "exp": datetime.now(timezone.utc) + timedelta(hours=24)},
        settings.secret_key,
        algorithm=ALGO,
    )


def get_user_id(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGO])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError, TypeError):
        return None
