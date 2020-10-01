from typing import Any
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from .. import deps, mail, orm, schemas


router = APIRouter()


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: orm.models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    mail.send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
