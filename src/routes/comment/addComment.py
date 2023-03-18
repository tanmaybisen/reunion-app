# •	POST /api/comment/{id} 
# add comment for post with {id} by the authenticated user.
# o	Input: Comment
# o	Return: Comment-ID

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from models.CommentAdd import CommentAdd
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

addCommentRouter = APIRouter()

# POST - To add comment
@addCommentRouter.post("/api/comment/{id}", tags=['Comments'])
async def commentOnPost(id, comment:CommentAdd, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    username = payload.get("username")

    if comment.comment=="" or comment.comment==None:
        return JSONResponse(content={'Abort':'Comment can\'t be empty'}, status_code=400)

    try:
        db=session()
        res=db.execute(text(f'INSERT INTO comments \
            ( \
                userid, \
                postid, \
                comment \
            ) \
            VALUES \
            ( \
                {userid}, \
                {id}, \
                \'{comment.comment}\' \
            ) RETURNING commentid')).fetchall()
        db.commit()
        return JSONResponse(content={'Comment-ID':res[0][0]}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'COMMENT request failed'}, status_code=401)
    finally:
        db.close()