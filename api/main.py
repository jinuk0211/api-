from typing import Optional
from pydantic import BaseModel, BaseSettings 
from fastapi.params import Body
from fastapi import FastAPI
from fastapi import Response, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  #CORS 미들웨어
from passlib.context import CryptContext
import random

from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine  
from schemas import *
from routers import auth, posts, users
from .config import settings
pwd_context = CryptContext(schemes=["bcrypt"]#bcrypt 암호화 방식
                           ,deprecated="auto"#암호화 방식
                            )




# models.Base.metadata.create_all(bind=engine)
    


app = FastAPI()

origins = [*]#모든 오리진을 허용
#['https://www.google.com','https://youtube.com']#허용할 오리진

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#모든 오리진을 허용
    allow_credentials=True,#인증
    allow_methods=["*"],#모든 메소드를 허용
    allow_headers=["*"],#모든 헤더를 허용
)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)


class post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None

#데이터베이스
 
myposts = [{"title":"title of post 1", "content":"content of post 1"}, {"title":"title of post 2", "content":"content of post 2"}]

def find_post(id):
    for post in myposts:
        if post['id'] == id:
            return post
    return None

def find_index_post(id):
    for index, post in enumerate(myposts):
        if post['id'] == id:
            return index
    return None

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/sqlalchemy')
def tests_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    print(posts)
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED, 
          response_model=schemas.Post #데이터베이스에서 가져올 데이터 형식
          )

def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content,published) VALUES (%s, %s. %s)",
    #                 (post.title, post.content,post.published ))
    # new_post = cursor.fetchone()

    # conn.commit()
    new_post  =models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#새로운 데이터베이스를 추가하고 나서 새로운 데이터베이스를 반환한다.
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="{id} 가 없습니다")

    return {'data':new_post}

@app.get('/posts/{id}') 
def get_post(id: int,response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {'postdetail':post}
    
@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    index = find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Post not found")
    myposts.pop(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int,  updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s RETURNING *",
    #                 (post.title, post.content, post.published))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)#데이터베이스에서 id를 찾는다.
    #업데이트할 데이터를 가져온다.
    post = post_query.first()#첫번째 데이터를 가져온다.


    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post('/users',status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate,
                 db: Session = Depends(get_db)#데이터베이스 연결
                 ):
    #유저 비밀번호 암호화
    hased_password =  utils.hash(user.password)
    user.password = hased_password


    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    #새로운 데이터베이스를 추가하고 나서 새로운 데이터베이스를 반환한다.
    return {'data':new_user}
