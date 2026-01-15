from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone: int

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True