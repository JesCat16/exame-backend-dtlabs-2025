from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from DB.dbconnection import SessionLocal
from Models.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

#Router for the auth methods
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Secret_key and algorith to create token
SECRET_KEY = 'ksj4v7o0bcvjcoabh3m47kkat3jimcbt63x2vt3thlut7tviw4hpdhdw6rhbot3z'
ALGORITHM = 'HS256'

# Encrypt password for the database registre
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

#Input for login and creation of token
class CreateUser(BaseModel):
    user_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Used to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#Register User
@router.post("/register", status_code= status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUser):
    create_user_model = User(
        user_name = create_user_request.user_name,
        password = bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()

#Generate token
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= 'Could not validate user. Check if user exists or if the password is correct')
    token = create_access_token(user.user_name, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

#Confirm if user exist
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.user_name == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

#Create token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta 
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

#Get user currently at used
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user. Check if user exists.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED)