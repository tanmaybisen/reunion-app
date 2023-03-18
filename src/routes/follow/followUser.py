from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

followUserRouter = APIRouter()

# POST - To add connection
@followUserRouter.post("/api/follow/{id}", tags=['Follow-Unfollow'])
async def followUser(id, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    username = payload.get("username")
    
    if userid==int(id):
        return JSONResponse(content={'Abort':'Self-follow not allowed'}, status_code=400)
    
    try:
        db=session()
        
        res=db.execute(text(f'INSERT INTO connections \
            ( \
                userid, \
                friendid \
            ) \
            VALUES \
            ( \
                {userid}, \
                {id} \
            ) \
            ON CONFLICT (userid, friendid) DO NOTHING'))
        db.commit()
        return JSONResponse(content={'Success':f'{username} follows person with ID={id}'}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'FOLLOW request failed'}, status_code=401)
    finally:
        db.close()