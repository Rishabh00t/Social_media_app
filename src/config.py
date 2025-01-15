class Settings:
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    MAIL_FROM: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    USE_CREDENTIALS: bool

    class Config:
        env_file = ".env"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rishabh@localhost:5433/test1"

SECRET_KEY = "HyySecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 10