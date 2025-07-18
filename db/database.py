from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Using Session
# with Session.begin() as session:
#     session.add(some_object)
#     session.add(some_other_object)
# # commits the transaction, closes the session
