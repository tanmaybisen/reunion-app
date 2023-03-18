from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from models.PostAdd import PostAdd
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

addPostRouter = APIRouter()

# POST - To add connection
@addPostRouter.post("/api/posts/", tags=['Posts'])
async def addPost(post: PostAdd, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    username = payload.get("username")
    
    if post.title=="":
        return JSONResponse(content={'Oops!':'Title can not be empty.'}, status_code=400)
    if post.description=="":
        return JSONResponse(content={'Oops!':'Description can not be empty.'}, status_code=400)
    
    try:
        db=session()
        
        res=db.execute(text(f'INSERT INTO posts \
            ( \
                authorid, \
                title, \
                description \
            ) \
            VALUES \
            ( \
                {userid}, \
                \'{post.title}\', \
                \'{post.description}\' \
            ) \
            RETURNING postid, title, description, created_at')).fetchall()
        db.commit()
        return JSONResponse(content={
                "Post-ID":res[0][0],
                "Title":res[0][1],
                "Description":res[0][2],
                "Created Time(UTC)":str(res[0][3])
            }, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'Post request failed'}, status_code=401)
    finally:
        db.close()