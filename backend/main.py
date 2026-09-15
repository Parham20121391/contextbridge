from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, summarize, projects
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="ContextBridge", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(summarize.router, prefix="/api/summarize", tags=["Summarize"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("../frontend/templates/index.html")