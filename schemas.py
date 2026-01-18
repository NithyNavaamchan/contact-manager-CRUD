from pydantic import BaseModel, Field, field_validator
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str

@field_validator("phone")
def validate_phone(cls, v):
    if not v.isdigit():
        raise ValueError("Phone number must contain only digits")
    if len(v) != 10:
        raise ValueError("Phone number must be exactly 10 digits long")

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True