# •	GET api/posts/{id} 
# would return a single post with {id} populated with its number of likes and comments

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

getPostRouter = APIRouter()

# POST - Get Post
@getPostRouter.get("/api/posts/{id}", tags=['Posts'])
async def getPost(id, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")

    try:
        db=session()
        
        post_exists=db.execute(text(f"SELECT COUNT(postid) \
            FROM posts \
            WHERE postid={id}")).fetchall()
        
        if post_exists[0][0]==0:
            return JSONResponse(content={'Error':'Post dosen\'t exists'}, status_code=400)
        
        likes=db.execute(text(f"SELECT COUNT(status) \
            FROM like_dislike \
            WHERE status = 'LIKE' AND postid={id}")).fetchall()
        
        comments=db.execute(text(f"SELECT comment \
            FROM comments \
            WHERE postid = {id} ")).fetchall()
        db.commit()
            
        return JSONResponse(content={
                "number of likes":likes[0][0],
                "comments":[curr[0] for curr in comments]
            }, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'GET request failed'}, status_code=401)
    finally:
        db.close()