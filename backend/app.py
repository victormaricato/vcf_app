from typing import Optional, Union

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, models
from .database.repository import query_by_chr_and_pos, query_by_rsid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/query", response_model=models.PydanticVariant)
def query(query: str, db: Session = Depends(get_db)) -> models.PydanticVariant:
    """
    Given an query of chromosome, position or rsid, return the variant from the database.
    Args:
        query: Can be either a two strings, consisting of chromosome and position, or a single string, which should be the RSID.

    Returns:
        Loaded variant from the database.
    """
    parsed_query = _parse_query(query)
    variant = _get_variant_by_query(db, parsed_query)
    if not variant:
        raise ValueError(f"Invalid query {query}")
    return variant


def _parse_query(q: str) -> Union[str, list[str]]:
    return q.split(" ")


def _get_variant_by_query(db: Session, parsed_query: Union[str, list[str]]) -> Optional[models.PydanticVariant]:
    if _is_chr_and_pos(parsed_query):
        chromosome, position = parsed_query
        return query_by_chr_and_pos(db, chromosome, position)
    if _is_rsid(parsed_query):
        rsid = parsed_query[0]
        return query_by_rsid(db, rsid)


def _is_rsid(parsed_query: Union[str, list[str]]) -> bool:
    return len(parsed_query) == 1


def _is_chr_and_pos(parsed_query: Union[str, list[str]]) -> bool:
    return len(parsed_query) == 2
