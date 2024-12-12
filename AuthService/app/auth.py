from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import schemas, crud, database ,models
from jwt import encode, decode ,ExpiredSignatureError
from datetime import datetime, timedelta
import os
from .crud import pwd_context

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "926e3c3b282f22e6c09ed7f3824deedc37993d40e6f90c08c2bc07cbf710fca6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 刷新令牌
@router.post("/refresh")
def refresh(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        new_access_token = create_access_token(data={"sub": email})
        return {"access_token": new_access_token}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

# 修改用户数据
@router.put("/user/update")
def update_user(email: str, password: str, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_email = payload.get("sub")
        if current_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        hashed_password = pwd_context.hash(password)
        user = db.query(models.User).filter(models.User.email == email).first()
        user.email = email
        user.hashed_password = hashed_password
        db.commit()
        return {"msg": "User data updated successfully"}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

# 查看用户历史
@router.get("/user/history")
def user_history(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"msg": "User history retrieved"}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"msg": "User logged out"}