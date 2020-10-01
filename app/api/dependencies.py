from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from .. import schemas, orm, auth, config


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = orm.SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> orm.models.User:
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[auth.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = orm.users.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: orm.models.User = Depends(get_current_user),
) -> orm.models.User:
    if not orm.users.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: orm.models.User = Depends(get_current_user),
) -> orm.models.User:
    if not orm.users.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
