from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from models import User
from schemas import UserCreate


#create user
def create_user(db: session, user: UserCreate):
    try:
        db_user = User(name=user.name, phone=user.phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise

#get all user
def get_users(db:session, skip:int=0, limit:int=20):
    return db.query(User).offset(skip).limit(limit).all()

#get user by id
def get_user_by_id(db:session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

#update user
def update_user(db:session, user_id:int, user: UserCreate):
    try: 
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db_user.name = user.name
        db_user.phone = user.phone
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        return None

#delete user
def delete_user(db:session, user_id:int):
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db.delete(db_user)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False