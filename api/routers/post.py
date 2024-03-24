from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session #데이터베이스 세션
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db
router = APIRouter(
    prefix="/posts",
    tags=["posts"],

)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10,#한번에 가져올 데이터의 수
              skip: int = 0,#데이터를 건너뛸 수
              search: Optional[str] = ''
              ):
    
    posts = db.query(models.Post).filter().limit(limit).offset(skip).all()
    
    return posts
