# •	POST /api/like/{id} 
# would like the post with {id} by the authenticated user.

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

likeRouter = APIRouter()

# POST - like a post
@likeRouter.post("/api/like/{id}", tags=['Like-Dislike'])
async def likePost(id, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")

    try:
        db=session()
        res=db.execute(text(f"INSERT INTO like_dislike \
            ( \
                userid, \
                postid, \
                status \
            ) \
            VALUES \
            ( \
                {userid}, \
                {id}, \
                'LIKE' \
            ) \
            ON CONFLICT (userid, postid) DO UPDATE \
            SET \
            status = 'LIKE' \
            "))
        db.commit()
        return JSONResponse(content={'Success':f'You liked post ID:{id}'}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'Like request failed'}, status_code=401)
    finally:
        db.close()