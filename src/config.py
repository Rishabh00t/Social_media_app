import os
from dotenv import load_dotenv

load_dotenv()

# class Settings:
#     EMAIL_USERNAME: str
#     EMAIL_PASSWORD: str
#     SMTP_SERVER: str
#     SMTP_PORT: int
#     MAIL_FROM: str
#     MAIL_TLS: bool
#     MAIL_SSL: bool
#     USE_CREDENTIALS: bool

# SECRET_KEY = "HyySecret"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 10
# REFRESH_TOKEN_EXPIRE_DAYS = 10

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    DB_URL = os.getenv("DATABASE_URL")