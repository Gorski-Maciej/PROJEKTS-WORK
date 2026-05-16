import os, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY=os.getenv('JWT_SECRET','supersecretkey')
ALGO='HS256'
oauth2=OAuth2PasswordBearer(tokenUrl='/token')
USERS={'admin':{'password':'admin123','role':'admin'},'viewer':{'password':'viewer123','role':'readonly'}}

def create_access_token(data, expires_delta=None):
    payload=data.copy(); payload['exp']=datetime.now(timezone.utc)+(expires_delta or timedelta(hours=2))
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

async def verify_token(token:str=Depends(oauth2)):
    try: return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except Exception as e: raise HTTPException(status_code=401, detail=str(e))
