from typing import Optional


from pydantic import BaseModel, computed_field


class LoggedInUser(BaseModel):
    username: str
    user_no: int


class BandRead(BaseModel):
    id: int
    name: str

    @computed_field
    def band_url(self) -> str:
        return f"https://band.us/band/{self.id}"


class CreateComment(BaseModel):
    band_id: str
    post_id: str
    my_comment: str
    my_name: str
    check_message: Optional[str] = None
