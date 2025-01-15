from fastapi_mail import ConnectionConfig
from passlib.context import CryptContext

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
