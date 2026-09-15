import json
from models.schemas import Conversation, Message
from typing import Union

def parse_claude_export(data: dict) -> Conversation:
    messages = []
    for msg in data.get("chat_messages", []):
        content = ""
        if isinstance(msg.get("content"), list):
            for block in msg["content"]:
                if block.get("type") == "text":
                    content += block.get("text", "")
        elif isinstance(msg.get("content"), str):
            content = msg["content"]
        messages.append(Message(
            role=msg.get("sender", "user"),
            content=content,
            timestamp=msg.get("created_at")
        ))
    return Conversation(
        source="claude",
        title=data.get("name", "Claude Conversation"),
        messages=messages,
        exported_at=data.get("created_at")
    )

def parse_chatgpt_export(data: dict) -> Conversation:
    messages = []
    mapping = data.get("mapping", {})
    for node_id, node in mapping.items():
        msg = node.get("message")
        if not msg:
            continue
        role = msg.get("author", {}).get("role", "")
        if role not in ["user", "assistant"]:
            continue
        content_parts = msg.get("content", {}).get("parts", [])
        content = " ".join([p for p in content_parts if isinstance(p, str)])
        if content.strip():
            messages.append(Message(
                role=role,
                content=content,
                timestamp=str(msg.get("create_time", ""))
            ))
    return Conversation(
        source="chatgpt",
        title=data.get("title", "ChatGPT Conversation"),
        messages=messages
    )

def detect_and_parse(raw: Union[dict, list]) -> Conversation:
    if isinstance(raw, list) and raw and "mapping" in raw[0]:
        return parse_chatgpt_export(raw[0])
    if isinstance(raw, dict):
        if "chat_messages" in raw:
            return parse_claude_export(raw)
        elif "mapping" in raw:
            return parse_chatgpt_export(raw)
    raise ValueError("فرمت فایل شناخته نشد. لطفاً export از Claude یا ChatGPT آپلود کنید.")