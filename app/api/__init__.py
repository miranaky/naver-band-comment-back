from api.comment import router as comment_router
from api.users import router as users_router
from fastapi import APIRouter

router = APIRouter(prefix="/api")

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(comment_router, prefix="/comment", tags=["comment"])
