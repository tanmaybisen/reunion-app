from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.authentication.login import loginRouter
from routes.authentication.userDetails import userDetailsRouter
from routes.follow.followUser import followUserRouter
from routes.follow.unfollowUser import unfollowUserRouter
from routes.post.addPost import addPostRouter
from routes.post.deletePost import delPostRouter
from routes.like.likePost import likeRouter
from routes.like.dislikePost import dislikeRouter
from routes.comment.addComment import addCommentRouter
from routes.post.getPost import getPostRouter
from routes.post.getAllPosts import getAllPostRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',tags=['Check'])
def root_route():
    return {'Success':'UP and RUNNING'}

app.include_router(loginRouter)
app.include_router(userDetailsRouter)
app.include_router(followUserRouter)
app.include_router(unfollowUserRouter)
app.include_router(addPostRouter)
app.include_router(delPostRouter)
app.include_router(likeRouter)
app.include_router(dislikeRouter)
app.include_router(addCommentRouter)
app.include_router(getPostRouter)
app.include_router(getAllPostRouter)