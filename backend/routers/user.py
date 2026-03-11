from fastapi import APIRouter, Depends
from dependencies import get_admin_user

router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)

@router.get("/requests")
def get_user_requests(admin: dict = Depends(get_admin_user)):
    """
    Temporary endpoint returning an empty list for pending user requests.
    """
    return []
