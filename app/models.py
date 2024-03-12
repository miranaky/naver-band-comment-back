from typing import Optional

from pydantic import BaseModel


class CreateComment(BaseModel):
    band_id: str
    post_id: str
    my_comment: str
    tag: bool = True
    new: bool = True
    my_name: Optional[str] = None
    check_message: Optional[str] = None
