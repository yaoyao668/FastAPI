from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import encode, decode ,ExpiredSignatureError
import os
from .auth import create_access_token
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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