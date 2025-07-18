from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorReadSchema)
def create_author(author_data: schemas.AuthorBaseSchema, session: Session = Depends(get_db)):
    author = crud.get_author_by_name(session=session, name=author_data.name)
    if author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with this name {author.name} already exist!"
        )
    return crud.create_author(session=session, author_data=author_data)


@app.get("/authors/", response_model=list[schemas.AuthorReadSchema])
def get_author_list(
        skip: int = 0,
        limit: int = 10,
        session: Session = Depends(get_db),
):
    return crud.get_list_author(session=session, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookReadSchema)
def create_book_view(book: schemas.BookBaseSchema, session: Session = Depends(get_db)):
    return crud.create_book(session=session, book=book)
