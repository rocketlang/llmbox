from fastapi import FastAPI
from pydantic import BaseModel
from ..router.core import LLMBox

class ChatIn(BaseModel):
    messages: list[dict]
    provider: str | None = None
    max_tokens: int | None = None

api = FastAPI(title="LLMBox API", version="0.1.0")

@api.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}

@api.post("/v1/chat/completions")
async def chat_route(payload: ChatIn):
    text = ""
    for m in reversed(payload.messages):
        if m.get("role") == "user":
            text = m.get("content","")
            break
    resp = await LLMBox.a_chat(text, provider=payload.provider, max_tokens=payload.max_tokens)
    return {
        "choices":[{"message":{"role":"assistant","content":resp.content}}],
        "usage":{"total_cost_usd":resp.cost.usd}
    }
