from fastapi import APIRouter

router = APIRouter()

from database.config import db

@router.get("/")
def get_all_candidats():
    return db.query("SELECT * FROM CANDIDATS;")


@router.get("/{id}")
def get_candidat_by_id(id: int):
    return db.query(f"SELECT * FROM CANDIDATS WHERE ID_CANDIDAT = {id};")