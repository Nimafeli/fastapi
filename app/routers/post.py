from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)

# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
# @router.get('/')
async def get_posts(db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user),
                    limit : int = 5, skip : int = 0, search : Optional[str] = ""):
    #WORKING WITH SQL
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #WORKING WITH ORM
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post('/', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    #WORKING WITH SQL
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # print(new_post)

    # conn.commit()


    #WORKING WITH ORM
    new_post  = models.Post(owner_id=current_user.id, **post.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
async def get_post(id : int, db : Session = Depends(get_db), currnet_user : schemas.User = Depends(oauth2.get_current_user)):
    # post = getPost(id)

    #WORKING WITH SQL
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'we can\'t find id = {id} in database!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f'we can\'t find id: {id} in database!'}

    #WORKING WITH ORM
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.user_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'we can\'t find id: {id} in database!')
    
    return post


@router.delete('/{id}')
async def delete_post(id: int, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    # index = find_post_index(id)
    # print(index)
    # if index == None:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #                         detail= 'we can\'t find this post')
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    #WORKING WITH SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    # print(post)
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="There is not post with this id")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    # index = find_post_index(id)

    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                   detail= 'we can\'t find this post!')

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return{'data': post_dict}


    #WORKING WITH SQL
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"There is no id like {id}")
    
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    updated_post.update(post.__dict__,synchronize_session=False)
    
    db.commit()
    return updated_post.first()