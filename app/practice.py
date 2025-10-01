#until part 15 exercise


# from fastapi import FastAPI
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional
# from random import randrange



# app = FastAPI()

# class Post(BaseModel):
#   title: str
#   content: str
#   rating: Optional[int] = None
#   published: bool = True


# posts = [{'title': 'Nima', 'content': 'Nima is from marand', 'id': 5},
#          {'title': 'mamad', 'content': 'mamad is from semnan', 'id': 10}]


# @app.get("/")
# async def root():
#   return{'data': 'hello how are you'}


# @app.get("/posts")
# async def get_posts():
#   return{'data': posts}

# @app.post("/posts")
# async def create_posts(post: Post):
#   dict_post = post.dict()
#   dict_post['id'] = randrange(0, 10000000)
#   posts.append(dict_post)
#   return{'data': dict_post}






#connecting database to fastai exercise

# from fastapi import FastAPI, Depends
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from fastapi import HTTPException,status, Response
# from . import modals
# from .database import engine, SessionLocal
# from sqlalchemy.orm import Session

# modals.Base.metadata.create_all(bind = engine)

# app = FastAPI()

# def get_db():
#   db = SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()

# class Post(BaseModel):
#   title: str
#   content: str
#   published: bool = True


# while True:
#   try:
#     conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="Nima2325!"
#                             ,cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("connection was succesfull!")
#     break
#   except Exception as error:
#     print('connection was unsuccesfull!')
#     print('error was', error)
#     time.sleep(5)
    


# @app.get("/")
# async def root():
#   return{'data': 'hello how are you'}


# @app.get("/posts")
# async def getPosts():
#   cursor.execute("""SELECT * FROM posts""")
#   posts = cursor.fetchall()
#   return{'data': posts}


# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#   return{"status": "succes "}


# @app.get('/posts/{id}')
# async def getPost(id: int):
#   cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
#   post = cursor.fetchone()
#   if not post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post whit id = {id}")
  
#   return{'data': post}


# @app.post('/posts')
# async def createPost(post : Post):
#   cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#                   (post.title, post.content, post.published))
#   created_post = cursor.fetchone()
#   conn.commit()
#   return{'data': created_post}


# @app.delete('/posts/{id}')
# async def deletePost(id: int):
#   cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
#   deleted_post = cursor.fetchone()
#   if not deleted_post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post with id like {id}")
  
#   return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put('/posts/{id}')
# async def updatePost(id : int, post: Post):
#   cursor.execute("""UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""",
#                  (post.title, post.content, post.published, str(id)))
  
#   updated_post = cursor.fetchone()
#   conn.commit()
#   if not updated_post :
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post with id like {id}")
  
#   return{'data': updated_post}





#UNTIL 5:45 OF MOVIE

# from fastapi import FastAPI,Depends, HTTPException, status, Response
# from sqlalchemy import create_engine, Column, String, Integer, Boolean
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
# from pydantic import BaseModel, ConfigDict
# app = FastAPI()


# SQLALCHEMY_URL = "postgresql+psycopg2://postgres:Nima2325!@localhost/fastapi"
# engine = create_engine(SQLALCHEMY_URL)
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Base = declarative_base()

# class Post(Base):
#   __tablename__ = 'posts'

#   id = Column(Integer, nullable=True, primary_key=True)
#   title = Column(String, nullable=True)
#   content = Column(String, nullable=True)
#   published = Column(Boolean, server_default='TRUE', nullable=False)
#   created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))

# Base.metadata.create_all(engine)

# def get_db():
#   db = SessionLocal()
#   try: 
#     yield db
#   finally:
#     db.close()



# class PostCreate(BaseModel):
#   title : str
#   content : str
#   published : bool = False


# class RespondPost(PostCreate):
#   model_config = ConfigDict(from_attributes=True)


# @app.get('/posts')
# async def getPosts(db : Session = Depends(get_db)):
#   posts = db.query(Post).all()
#   return {'data': posts}



# @app.get('/posts/{id}')
# async def getPost(id: int, db: Session = Depends(get_db)):
#   post = db.query(Post).filter(Post.id == id).first()
#   if not post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post wit id = {id}")
  
#   return{'data': post}


# @app.post('/posts')
# async def createPost(post : PostCreate, db : Session = Depends(get_db)):
#   created_post = Post(**post.__dict__)
#   db.add(created_post)
#   db.commit()
#   db.refresh(created_post)

#   return{'data': created_post}


# @app.delete('/posts/{id}')
# async def deletePost(id : int, db : Session = Depends(get_db)):
#   post = db.query(Post).filter(Post.id == id)
#   if not post.first():
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post wiht id = {id}")
  
#   post.delete(synchronize_session=False)
#   db.commit()

#   return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put('/posts/{id}', response_model=RespondPost)
# async def updatePost(post : PostCreate, id: int, db: Session = Depends(get_db)):
#   updated_post = db.query(Post).filter(Post.id == id)
#   if not updated_post.first():
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"There is no post like id = {id}")
  
#   updated_post.update(post.__dict__,synchronize_session=False)
#   db.commit()

#   return updated_post.first()


