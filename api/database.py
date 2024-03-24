from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
import psycopg2
from psycopg2.extras import RealDictCursor#데이터베이스에서 데이터를 딕셔너리 형태로 가져올 수 있게 해줌
import time
from .config import settings
                                    #유저네임, 비밀번호, (ip주소, 호스트이름),포트 데이터베이스 이름    
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine  = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try : 
        conn = psycopg2.connect(host = 'localhost', dbname = 'fastapi',
                                user = 'postgres', password = 'password123',
                                cursor_factory = psycopg2.extras.RealDictCursor)
        cursor = conn.cursor()
        print("데이터 베이스 연결됨")
        break
    except Exception as error:
        print('connection error')
        print(error)
        time.sleep(1)
