from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
from models import Base, User
from schemas import UserCreate, UserResponse
import user_service

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from sqlalchemy.exc import SQLAlchemyError
from exceptions import db_exception_handler, generic_exception_handler

app = FastAPI()


#rate limiter setup
Limiter = Limiter(key_func=get_remote_address)
app.state.limiter = Limiter

app.add_exception_handler(
    RateLimitExceeded,
    lambda r, e: JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."},
    )
)

#global exception
app.add_exception_handler(SQLAlchemyError, db_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

#DB initialization
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#health check
@app.get("/health")
def helth_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return{"status": "up", "database": "connected"}
    except:
        return{"status": "up", "database": "disconnected"}


#create user
@app.post("/users", response_model=UserResponse)
@Limiter.limit("5/minute")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = user_service.create_user(db, user)
    if not result:
        raise HTTPException(status_code=503, detail="DB error")
    return result

#read users
@app.get("/users", response_model=list[UserResponse])
@Limiter.limit("10/minute")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip, limit)

#read user by id
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#update user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

#delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = user_service.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



