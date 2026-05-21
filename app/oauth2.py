from jose import JWTError ,jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status,Depends
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "AIODFA[SFJASJFKDA2DFADF\7737\\adfjaskfjsafasfsf]"
EXPIRATION_TIME = 10
ALGORITHM = "HS256"

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        id:str = payload.get("user_id")

        if not id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bad Token")
        
        token_data = TokenData(id = id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token=token, credentials_exception = credentials_exception)
