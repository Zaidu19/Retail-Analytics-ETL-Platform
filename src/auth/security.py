
from fastapi import HTTPException,status
from pwdlib import PasswordHash
from datetime import datetime,timezone,timedelta
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer

from src.config import(
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


password_hash = PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return password_hash.verify(password,hashed_password)


def create_access_token(data:dict)->str:
    to_encode =data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token:str)->dict:
    try:
        payload =jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token.") 
     


