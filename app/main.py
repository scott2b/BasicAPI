#from datetime import datetime, timedelta
#from typing import Optional, List
#import databases
#import sqlalchemy

#from fastapi import Depends, FastAPI, HTTPException, status

#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jose import JWTError, jwt
#from passlib.context import CryptContext
#from pydantic import BaseModel


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .config import settings
from .api.api_v1.api import api_router

#DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

#database = databases.Database(DATABASE_URL)
#metadata = sqlalchemy.MetaData()


#notes = sqlalchemy.Table(
#    "notes",
#    metadata,
#    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#    sqlalchemy.Column("text", sqlalchemy.String),
#    sqlalchemy.Column("completed", sqlalchemy.Boolean),
#)

#engine = sqlalchemy.create_engine(
#    DATABASE_URL, connect_args={"check_same_thread": False}
#)
#metadata.create_all(engine)


#class NoteIn(BaseModel):
#    text: str
#    completed: bool


#class Note(BaseModel):
#    id: int
#    text: str
#    completed: bool


# to get a string like this run:
# openssl rand -hex 32
#SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#ALGORITHM = "HS256"
#SECRET_KEY = 
#ACCESS_TOKEN_EXPIRE_MINUTES = 30


#fake_users_db = {
#    "johndoe": {
#        "username": "johndoe",
#        "full_name": "John Doe",
#        "email": "johndoe@example.com",
#        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#        "disabled": False,
#    }
#}


#class Token(BaseModel):
#    access_token: str
#    token_type: str


#class TokenData(BaseModel):
#    username: Optional[str] = None


#class User(BaseModel):
#    username: str
#    email: Optional[str] = None
#    full_name: Optional[str] = None
#    disabled: Optional[bool] = None


#class UserInDB(User):
#    hashed_password: str


#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()
app = FastAPI(
    title='BasicAPI',
    description='This is just a starter project',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/'
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

#@app.on_event("startup")
#async def startup():
#    await database.connect()


#@app.on_event("shutdown")
#async def shutdown():
#    await database.disconnect()


#@app.get("/notes/", response_model=List[Note])
#async def read_notes():
#    query = notes.select()
#    return await database.fetch_all(query)


#@app.post("/notes/", response_model=Note)
#async def create_note(note: NoteIn):
#    query = notes.insert().values(text=note.text, completed=note.completed)
#    last_record_id = await database.execute(query)
#    return {**note.dict(), "id": last_record_id}


#def verify_password(plain_password, hashed_password):
#    return pwd_context.verify(plain_password, hashed_password)


#def get_password_hash(password):
#    return pwd_context.hash(password)


#def get_user(db, username: str):
#    if username in db:
#        user_dict = db[username]
#        return UserInDB(**user_dict)


#def authenticate_user(fake_db, username: str, password: str):
#    user = get_user(fake_db, username)
#    if not user:
#        return False
#    if not verify_password(password, user.hashed_password):
#        return False
#    return user


#def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#    to_encode = data.copy()
#    if expires_delta:
#        expire = datetime.utcnow() + expires_delta
#    else:
#        expire = datetime.utcnow() + timedelta(minutes=15)
#    to_encode.update({"exp": expire})
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt


#async def get_current_user(token: str = Depends(oauth2_scheme)):
#    credentials_exception = HTTPException(
#        status_code=status.HTTP_401_UNAUTHORIZED,
#        detail="Could not validate credentials",
#        headers={"WWW-Authenticate": "Bearer"},
#    )
#    try:
#        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#        username: str = payload.get("sub")
#        if username is None:
#            raise credentials_exception
#        token_data = TokenData(username=username)
#    except JWTError:
#        raise credentials_exception
#    user = get_user(fake_users_db, username=token_data.username)
#    if user is None:
#        raise credentials_exception
#    return user


#async def get_current_active_user(current_user: User = Depends(get_current_user)):
#    if current_user.disabled:
#        raise HTTPException(status_code=400, detail="Inactive user")
#    return current_user


#@app.post("/token", response_model=Token)
#async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#    if not user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Bearer"},
#        )
#    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#    access_token = create_access_token(
#        data={"sub": user.username}, expires_delta=access_token_expires
#    )
#    return {"access_token": access_token, "token_type": "bearer"}


#@app.get("/users/me/", response_model=User)
#async def read_users_me(current_user: User = Depends(get_current_active_user)):
#    return current_user


#@app.get("/users/me/items/")
#async def read_own_items(current_user: User = Depends(get_current_active_user)):
#    return [{"item_id": "Foo", "owner": current_user.username}]



app.include_router(api_router, prefix=settings.API_V1_STR)
