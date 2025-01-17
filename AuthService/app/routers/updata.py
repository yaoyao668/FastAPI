from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import encode, decode ,ExpiredSignatureError
from app.crud import pwd_context
from app import schemas, crud, database ,models
from sqlalchemy.orm import Session

import os
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# updata user data
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