from fastapi import APIRouter, HTTPException
from models.schemas import SummaryRequest
from services.summarizer import summarize_with_gemini, summarize_with_openrouter
from services.storage import load_conversation

router = APIRouter()

@router.post("/")
async def summarize(req: SummaryRequest):
    try:
        conv = load_conversation(req.conversation_id)
        if req.model == "gemini":
            return await summarize_with_gemini(conv, req.style)
        return await summarize_with_openrouter(conv, req.style)
    except FileNotFoundError:
        raise HTTPException(404, "مکالمه پیدا نشد")
    except Exception as e:
        raise HTTPException(500, f"خطا: {str(e)}")