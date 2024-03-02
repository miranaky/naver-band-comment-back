# sqlmodel 을 사용한 데이터베이스 연결

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine


class Database:
    sqlite_file_name = "database.db"

    def __init__(self) -> None:
        self.db_url = f"sqlite:///{self.sqlite_file_name}"
        self.engine = create_engine(self.db_url)
        self.session = sessionmaker(
            self.engine, autocommit=False, autoflush=False, class_=Session
        )

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self.engine)


database = Database()


def get_session() -> Session:
    with database.session() as session:
        yield session
