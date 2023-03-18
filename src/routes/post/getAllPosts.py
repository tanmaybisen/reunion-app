# •	GET /api/all_posts 
# would return all posts created by authenticated user sorted by post time.
# o	RETURN: For each post return the following values 
# 	id: ID of the post
# 	title: Title of the post
# 	desc: Description of the post
# 	created_at: Date and time when the post was created
# 	comments: Array of comments, for the particular post
# 	likes: Number of likes for the particular post


from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from routes.dependencies.db_connect import session, exc, text
from auth.auth_handler import decodeJWT

getAllPostRouter = APIRouter()

# POST - Get All Post
@getAllPostRouter.get("/api/all_posts", tags=['Posts'])
async def getAllPost(token: str = Depends(JWTBearer())):

    payload = decodeJWT(token)
    userid = payload.get("userid")

    try:
        db=session()
        
        allPosts=db.execute(text(f"SELECT postid, \
            title, \
            description, \
            created_at \
            FROM posts \
            WHERE authorid={userid} \
            ORDER BY created_at " )).fetchall()
        
        all_details=[]
        for row in allPosts:
            post_id=row[0]
            
            likes=db.execute(text(f"SELECT COUNT(status) \
            FROM like_dislike \
            WHERE postid = {post_id} AND status = 'LIKE' " )).fetchall()
            
            comments=db.execute(text(f"SELECT comment \
            FROM comments \
            WHERE postid={post_id} \
            ")).fetchall()
            
            comments_list=[curr[0] for curr in comments]
            all_details.append(dict(zip(['id', 'title', 'desc', 'created_at', 'likes', 'comments'], list(row)+[likes[0][0],comments_list])))
        return all_details
    except exc.SQLAlchemyError as e:
        # return {"value":str(e)}
        return JSONResponse(content={'Error':'GET request failed'}, status_code=401)
    finally:
        db.close()