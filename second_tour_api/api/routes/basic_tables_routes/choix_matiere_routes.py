from fastapi import APIRouter

router = APIRouter()

from database.config import db

@router.get("/")
def get_all_choix_matiere():
    return db.query("SELECT * FROM CANDIDATS;")


@router.get("/{id}")
def get_choix_matiere_by_id(id: int):
    return db.query(f"SELECT * FROM CHOIX_MATIERE WHERE ID_CHOIX_MATIERE = {id};")