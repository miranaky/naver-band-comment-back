from typing import Optional

from pydantic import BaseModel


class CreateComment(BaseModel):
    band_id: str
    post_id: str
    my_comment: str
    tag: bool = True
    new: bool = True
    view: bool = False
    my_name: Optional[str] = None
    check_message: Optional[str] = None
    image_file: Optional[str] = None
