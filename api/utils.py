from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"]#bcrypt 암호화 방식
                           ,deprecated="auto"#암호화 방식
                            )

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)