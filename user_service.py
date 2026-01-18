from sqlalchemy.orm import session
from models import User
from schemas import UserCreate


#create user
def create_user(db: session, user: UserCreate):
    db_user = User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#get all user
def get_users(db:session):
    return db.query(User).all()

#get user by id
def get_user_by_id(db:session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

#update user
def update_user(db:session, user_id:int, user: UserCreate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.name = user.name
    db_user.phone = user.phone
    db.commit()
    db.refresh(db_user)
    return db_user

#delete user
def delete_user(db:session, user_id:int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return True