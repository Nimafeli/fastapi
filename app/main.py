from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{'title': 'favorite foods', 'content': 'orange, apple, banana', 'id': 1},
#             {'title': 'the best places in Iran', 'content': 'Marand, Tehran, Tabriz, Mashhad', 'id': 2}]


# def getPost(id):
#     for p in my_posts:
#         if p['id'] == id:
#             print(p)
#             return p
        

# def find_post_index(id):
#     for i, p  in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
  return{'data': 'hello world'}

