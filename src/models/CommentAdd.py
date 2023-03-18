from pydantic import BaseModel, Field

class CommentAdd(BaseModel):
    comment: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "comment": "Stunning! Fab!"
            }
        }