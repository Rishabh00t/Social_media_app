from fastapi_mail import ConnectionConfig
from passlib.context import CryptContext
from datetime import datetime,timedelta
from fastapi import HTTPException,status
import jwt
from src.config import Config

conf = ConnectionConfig(    
    MAIL_USERNAME='rishabh317.rejoice@gmail.com',
    MAIL_PASSWORD='auji cnck oqek yumn',
    MAIL_FROM='rishabh317.rejoice@gmail.com',
    MAIL_PORT=465,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_key =Config.SECRET_KEY
algorithm = Config.ALGORITHM
access_token = Config.ACCESS_TOKEN
refresh_token = Config.REFRESH_TOKEN


def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_token)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def create_refresh_token(data:dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=refresh_token)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

