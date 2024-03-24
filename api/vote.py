from fastapi import APIRouter, HTTPException, FastAPI, Depends, Request, status, Session,     
from .. import schemas, models, database, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(database.get_db),
          current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Post).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    found_vote = vote_query.first()

  
    # if vote.dir == 1:
    #     post.vote_count += 1

    # elif vote.dir == -1:
    #     post.vote_count -= 1

    # db.commit()
    return {"detail": "Vote added"}