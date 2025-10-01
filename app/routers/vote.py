from fastapi import APIRouter, status, Depends, HTTPException, Response
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/vote",
  tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == 
                                 current_user.id)
  found_vote = vote_query.first()

  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"There is no post with id {vote.post_id}")
  if (vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                          detail=f"user {current_user.id} has already voted on post {vote.post_id}")
    new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail="Vote does not exite")
    
    vote_query.delete(synchronize_session=False)
    db.commit()
  return{"message": "successfully added vote"}


 