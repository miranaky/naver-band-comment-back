from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: str = Field(primary_key=True)
    content: str
    band_id: str = Field(index=True)
    comments_count: str
    view_count: str
    created_at: str


class Comment(SQLModel):
    id: str = Field(primary_key=True)
    post_id: str = Field(index=True)
    user_name: str = Field(index=True)
    content: str
    parent_comment_id: str = Field(default=None, index=True)
    is_replied: bool = Field(default=False)


class Band(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
