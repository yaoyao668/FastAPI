from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import encode, decode ,ExpiredSignatureError


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"msg": "User logged out"}