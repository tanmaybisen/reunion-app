from pydantic import BaseModel, Field

class CustomerLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "tanmay@reunion.org",
                "password": "tanmay"
            }
        }