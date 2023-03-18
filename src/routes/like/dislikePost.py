# •	POST /api/unlike/{id} 
# would unlike the post with {id} by the authenticated user.

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

dislikeRouter = APIRouter()

# POST - unlike a post
@dislikeRouter.post("/api/unlike/{id}", tags=['Like-Dislike'])
async def unLikePost(id, token: str = Depends(JWTBearer())):

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
                'UNLIKE' \
            ) \
            ON CONFLICT (userid, postid) DO UPDATE \
            SET \
            status = 'UNLIKE' \
            "))
        db.commit()
        return JSONResponse(content={'Success':f'You unliked post ID:{id}'}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'UnLike request failed'}, status_code=401)
    finally:
        db.close()