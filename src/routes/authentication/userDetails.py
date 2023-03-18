from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

userDetailsRouter = APIRouter()

# GET - Get user details [username, followers, following]
@userDetailsRouter.get("/api/user", tags=['Login-UserDetails'])
async def getUserDetails(token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    username = payload.get("username")
    
    try:
        db=session()
        following=db.execute(text(f'SELECT COUNT(userid) \
            FROM connections \
            WHERE userid={userid}')).fetchall()
        followers=db.execute(text(f'SELECT COUNT(friendid) \
            FROM connections \
            WHERE friendid={userid}')).fetchall()
        db.commit()
        return JSONResponse(content={
                "username":username,
                "followers":followers[0][0],
                "following":following[0][0]
            }, status_code=200)
    except exc.SQLAlchemyError as e:
        return JSONResponse(content={'Error':'request failed'}, status_code=401)
    finally:
        db.close()