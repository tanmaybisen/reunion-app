from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from models.CustomerLogin import CustomerLogin
from auth.auth_handler import signJWT
from routes.dependencies.db_connect import session, exc, text

loginRouter = APIRouter()

# Function to validate user, by searching in DB
def check_user(data: CustomerLogin):
    try:
        db=session()
        user_data = db.execute(text(f'SELECT userid, \
                    username, \
                    email \
                    FROM users \
                    where email=\'{data.email}\' AND password=\'{data.password}\'')).fetchall()

        db.commit()
        user_details = [dict(zip(["userid","username","email"], row)) for row in user_data]
        if len(user_details)==1:
            return user_details
        else:
            return False
    except exc.SQLAlchemyError as e:
        # import warnings
        # warnings.warn(str(e))
        return e
    finally:
        db.close()
     
# Login Endpoint
@loginRouter.post("/api/authenticate", tags=["Login-UserDetails"])
async def user_login(user: CustomerLogin = Body(...)):
    response=check_user(user)

    if response!=False:
        token=signJWT(response)
        return {
                "token":token.get("token")
            }
    return JSONResponse(content={"Access Denied": "User not found"}, status_code=401)