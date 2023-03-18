from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

unfollowUserRouter = APIRouter()

# POST - To remove connection
@unfollowUserRouter.post("/api/unfollow/{id}", tags=['Follow-Unfollow'])
async def unfollowUser(id, token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")
    username = payload.get("username")
    
    if userid==int(id):
        return JSONResponse(content={'Abort':'Self-unfollow not allowed'}, status_code=400)

    try:
        db=session()
        res=db.execute(text(f'DELETE FROM connections \
            WHERE userid={userid} AND friendid={id}'))
        db.commit()
        return JSONResponse(content={'Success':f'{username} unfollowed person with ID={id}'}, status_code=200)
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'UnFOLLOW request failed'}, status_code=401)
    finally:
        db.close()