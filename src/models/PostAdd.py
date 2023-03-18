from pydantic import BaseModel, Field

class PostAdd(BaseModel):
    title: str = Field(...)
    description: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Happy hours.",
                "description": "Default description add for this post."
            }
        }