from typing import Annotated

from fastapi import FastAPI, Query, HTTPException
from sqlmodel import select

from db.database import create_db_and_tables, SessionDep
from db.models import Author

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/authors/")
def create_author(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/authors/")
def read_authors(
    session: SessionDep,
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Author]:
    authors = session.exec(select(Author).offset(skip).limit(limit)).all()
    return authors


@app.get("/authors/{author_id}")
def read_author(author_id: int, session: SessionDep) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}
