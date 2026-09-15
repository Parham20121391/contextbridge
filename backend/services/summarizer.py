import os, httpx, json, re
from models.schemas import Conversation, SummaryResponse
from datetime import datetime

def build_conversation_text(conv: Conversation) -> str:
    return "\n\n".join([f"[{m.role.upper()}]: {m.content}" for m in conv.messages])

def build_prompt(conv_text: str, style: str) -> str:
    style_map = {
        "detailed": "یک خلاصه جامع و کامل بنویس.",
        "brief": "فقط مهم‌ترین نکات را در ۳-۴ جمله بنویس.",
        "bullets": "در قالب bullet point های کوتاه و واضح بنویس."
    }
    return f"""{style_map.get(style, "یک خلاصه جامع بنویس.")}

خروجی فقط JSON باشد بدون هیچ توضیح اضافه:
{{
  "summary": "خلاصه کامل مکالمه",
  "key_points": ["نکته ۱", "نکته ۲", "نکته ۳"],
  "ready_prompt": "prompt آماده برای session جدید"
}}

مکالمه:
{conv_text[:8000]}"""

async def summarize_with_gemini(conv: Conversation, style: str) -> SummaryResponse:
    key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    prompt = build_prompt(build_conversation_text(conv), style)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return _parse(text)

async def summarize_with_openrouter(conv: Conversation, style: str) -> SummaryResponse:
    key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
    prompt = build_prompt(build_conversation_text(conv), style)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}]}
        )
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
    return _parse(text)

def _parse(text: str) -> SummaryResponse:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            p = json.loads(match.group())
            return SummaryResponse(
                summary=p.get("summary", ""),
                key_points=p.get("key_points", []),
                ready_prompt=p.get("ready_prompt", ""),
                created_at=datetime.now().isoformat()
            )
        except: pass
    return SummaryResponse(summary=text, key_points=[], ready_prompt=text[:500], created_at=datetime.now().isoformat())