import json, uuid
from pathlib import Path
from datetime import datetime
from models.schemas import Conversation, Project

BASE = Path(__file__).parent.parent.parent
EXPORTS_DIR = BASE / "data" / "exports"
PROJECTS_DIR = BASE / "data" / "projects"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

def save_conversation(conv: Conversation) -> str:
    conv_id = str(uuid.uuid4())[:8]
    (EXPORTS_DIR / f"{conv_id}.json").write_text(conv.model_dump_json(indent=2), encoding="utf-8")
    return conv_id

def load_conversation(conv_id: str) -> Conversation:
    return Conversation.model_validate_json((EXPORTS_DIR / f"{conv_id}.json").read_text(encoding="utf-8"))

def list_conversations() -> list:
    result = []
    for f in EXPORTS_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        result.append({"id": f.stem, "title": data.get("title", "بدون عنوان"), "source": data.get("source", "unknown"), "message_count": len(data.get("messages", []))})
    return result

def save_project(project: Project) -> str:
    project.id = project.id or str(uuid.uuid4())[:8]
    project.created_at = project.created_at or datetime.now().isoformat()
    (PROJECTS_DIR / f"{project.id}.json").write_text(project.model_dump_json(indent=2), encoding="utf-8")
    return project.id

def list_projects() -> list:
    return [json.loads(f.read_text(encoding="utf-8")) for f in PROJECTS_DIR.glob("*.json")]