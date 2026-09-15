from fastapi import APIRouter, UploadFile, File, HTTPException
from services.parser import detect_and_parse
from services.storage import save_conversation, list_conversations
import json

router = APIRouter()

@router.post("/")
async def upload_export(file: UploadFile = File(...)):
    try:
        raw = json.loads(await file.read())
        conv = detect_and_parse(raw)
        conv_id = save_conversation(conv)
        return {"id": conv_id, "title": conv.title, "source": conv.source, "message_count": len(conv.messages)}
    except json.JSONDecodeError:
        raise HTTPException(400, "فایل JSON معتبر نیست")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/list")
async def get_conversations():
    return list_conversations()