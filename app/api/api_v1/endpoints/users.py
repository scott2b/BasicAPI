from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from .. import deps, config, orm, schemas


router = APIRouter()

DOCS = config.settings.DOCSET == 'full'


@router.get("/", response_model=List[schemas.User], include_in_schema=DOCS)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: orm.models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = orm.models.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, include_in_schema=DOCS)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: orm.models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = orm.models.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = orm.users.create(db, obj_in=user_in)
    if config.settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User, include_in_schema=True)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: orm.models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = orm.users.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User, include_in_schema=True)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: orm.models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User, include_in_schema=True)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not config.settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = orm.users.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = orm.users.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User, include_in_schema=DOCS)
def read_user_by_id(
    user_id: int,
    current_user: orm.models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = orm.users.get(db, id=user_id)
    if user == current_user:
        return user
    if not orm.users.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User, include_in_schema=DOCS)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: orm.models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = orm.users.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = orm.users.update(db, db_obj=user, obj_in=user_in)
    return user
