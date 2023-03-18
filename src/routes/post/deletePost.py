# •	DELETE api/posts/{id} 
# would delete post with {id} created by the authenticated user.

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

delPostRouter = APIRouter()

# POST - To add connection
@delPostRouter.delete("/api/posts/{id}", tags=['Posts'])
async def deletePost(id, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    
    try:
        db=session()
        res=db.execute(text(f'SELECT authorid \
            FROM posts \
            WHERE postid={id}')).fetchall()
        
        if res==[]:
            return JSONResponse(content={"Abort":"Post dosen't exists."}, status_code=400)
        
        if res[0][0]!=userid:
            return JSONResponse(content={"Abort":"You are not the author of this post."}, status_code=400)
        
        db.execute(text(f'DELETE FROM posts \
            WHERE authorid={userid} AND postid={id}'))
        db.commit()
        return JSONResponse(content={"Success":"Post Deleted"}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'Post request failed'}, status_code=401)
    finally:
        db.close()