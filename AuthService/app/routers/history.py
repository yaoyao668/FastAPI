from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import encode, decode ,ExpiredSignatureError

import os
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# get user history
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
