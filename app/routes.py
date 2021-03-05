# Framework imports
from fastapi import APIRouter

# Prefix Import
from . import API_PREFIX

from .db.engine import create_all
from .db.engine import drop_all

route = APIRouter()



@route.get("/")
def root():
    return {"message": "SBF Estoque - API"}


@route.get("/health")
def health_check():
    return {"message": "Health check ok."}


@route.get("/create-all")
def health_check():
    create_all()
    return {"message": "All tables created."}


@route.get("/drop-all")
def health_check():
    drop_all()
    return {"message": "Database dropped."}
