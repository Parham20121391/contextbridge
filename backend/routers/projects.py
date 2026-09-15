from fastapi import APIRouter
from models.schemas import Project
from services.storage import save_project, list_projects

router = APIRouter()

@router.post("/")
async def create_project(project: Project):
    return {"id": save_project(project), "message": "پروژه ذخیره شد"}

@router.get("/")
async def get_projects():
    return list_projects()