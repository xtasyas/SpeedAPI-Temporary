from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from speedapi.settings import DATABASE_URL

engine = create_engine(url=DATABASE_URL)


def get_session():
    with Session(bind=engine) as session:
        yield session
