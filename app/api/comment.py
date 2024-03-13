from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from service.comment import CreateCommentService

router = APIRouter()


@router.post("")
async def add_all_comment(
    create_comment: CreateCommentService = Depends(CreateCommentService),
):
    try:
        create_comment.create_comment()
    except Exception as e:
        HTTPException(status_code=400, detail=f"Failed to add comment ({e})")
    return JSONResponse(
        status_code=200,
        content={
            "message": "Comment added successfully.",
            "comments_count": create_comment.comments_count,
            "tagged_comments_count": create_comment.tagged_comments_count,
        },
    )
