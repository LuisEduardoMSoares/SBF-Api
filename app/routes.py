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
def create_all_tables():
    create_all()
    return {"message": "All tables created."}


@route.get("/drop-all")
def drop_all_content_on_database():
    drop_all()
    return {"message": "Database dropped."}
