from sqlalchemy.orm import Session

from .models import Variant


def query_by_chr_and_pos(db: Session, chr: str, pos: str) -> Variant:
    return db.query(Variant).filter((Variant.chromosome == chr) & (Variant.position == pos)).first()


def query_by_rsid(db: Session, rsid: str) -> Variant:
    return db.query(Variant).filter(Variant.rsid == rsid).first()
