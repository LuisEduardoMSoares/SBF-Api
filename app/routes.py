# Framework imports
from fastapi import APIRouter

# Prefix Import
from . import API_PREFIX

from .db.engine import create_all
from .db.engine import drop_all

router = APIRouter()



@router.get("/")
def root():
    return {"message": "SBF Estoque - API"}


@router.get("/health")
def health_check():
    return {"message": "Health check ok."}


@router.get("/create-all")
def health_check():
    create_all()
    return {"message": "All tables created."}


@router.get("/drop-all")
def health_check():
    drop_all()
    return {"message": "Database dropped."}
