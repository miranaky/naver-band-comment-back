from core.database import get_session
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from schema import Post
from service.post import get_latest_post_id_from_band, get_post_detail
from sqlalchemy import desc
from sqlmodel import select

router = APIRouter()


@router.get("/{band_id}")
async def get_post_list(
    band_id: str,
    offset: int = 0,
    limit: int = Query(default=20, le=100),
    session=Depends(get_session),
):
    posts = session.exec(
        select(Post)
        .where(Post.band_id == band_id)
        .order_by(desc(Post.id))
        .offset(offset)
        .limit(limit)
    ).all()
    return JSONResponse(
        content=[post.model_dump() for post in posts],
        media_type="application/json; charset=utf-8",
    )


@router.get(
    "/{band_id}/latest",
    name="Get latest post id from band.us",
)
async def get_latest_post_id(post_id: int = Depends(get_latest_post_id_from_band)):
    return {"latest": int(post_id)}


@router.put(
    "/{band_id}/post/{post_id}",
    name="Put post from band.us",
)
async def put_post(
    post: Post = Depends(get_post_detail),
    session=Depends(get_session),
):
    db_post = session.get(Post, post.id)
    if db_post:
        # Update the view count and comment count
        db_post.view_count = post.view_count
        db_post.comments_count = post.comments_count
        session.commit()
    else:
        db_post = post
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
    return db_post
