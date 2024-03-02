from fastapi import APIRouter

from app.api.band import router as band_router
from app.api.comment import router as comment_router
from app.api.post import router as post_router
from app.api.users import router as users_router

router = APIRouter()

router.include_router(band_router, prefix="/band", tags=["band"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(post_router, prefix="/post", tags=["post"])
router.include_router(comment_router, prefix="/comment", tags=["comment"])
