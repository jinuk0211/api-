from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, HTTPException, status, credentials_exception
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#로그인 url을 가져온다.
#키를 가져온다.
#알고리즘은 HS256
#exp는 만료시간
#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
SECRET_KEY = settings.secret_key#시크릿 키
#키
ALGORITHM = settings.algorithm#알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes#만료시간

def create_access_token(data: dict):
    to_encode = data.copy()
    #만료시간을 설정한다.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#토큰을 디코딩한다.
        id: int = payload.get("user_id")#id를 가져온다.
    
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)#토큰 데이터를 반환한다.
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credientials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail =f'could not validate credentials',
        headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credientials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user