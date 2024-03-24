from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import text, Timestamp, TIMESTAMP
#ForeignKey
#외래키

# 원격지에서 데이터베이스를 사용할 때는 아래와 같이 변경해야 한다.
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True,nullable=False)
    title = Column(String, index=True,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, default=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone= True),nullable=False,
                        server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id',
                                          ondelete='CASCADE'),
                                          nullable=False)#사용자가 삭제되면 게시물도 삭제))
class User(Base): #사용자 정보
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,
 ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    #ON DELETE CASCADE는 부모 테이블의 데이터를 삭제할 때, 
    # 연결된 자식 테이블의 데이터도 자동으로 함께 삭제하는 것을 의미.

    post_id = Column(Integer,
    ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
