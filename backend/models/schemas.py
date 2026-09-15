from pydantic import BaseModel
from typing import Optional, List

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class Conversation(BaseModel):
    source: str
    title: Optional[str] = None
    messages: List[Message]
    exported_at: Optional[str] = None

class SummaryRequest(BaseModel):
    conversation_id: str
    model: str = "gemini"
    style: str = "detailed"

class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    ready_prompt: str
    created_at: str

class Project(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    conversations: List[str] = []
    created_at: Optional[str] = None