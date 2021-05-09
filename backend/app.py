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
    parsed_query = parse_query(query)
    if len(parsed_query) == 2:
        chromosome, position = parsed_query
        return query_by_chr_and_pos(db, chromosome, position)
    if len(parsed_query) == 1:
        rsid = parsed_query[0]
        return query_by_rsid(db, rsid)
    raise ValueError(f"Invalid query {q}")


def parse_query(q: str) -> Union[str, list[str]]:
    return q.split(" ")
