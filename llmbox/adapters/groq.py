import httpx, os
from .base import Provider, ChatRequest, ChatResponse
from ..utils.cost import Cost
from ..utils.config import SETTINGS

class GroqProvider(Provider):
    name = "groq"
    free_tier = True

    async def chat(self, req: ChatRequest) -> ChatResponse:
        api_key = SETTINGS.groq_api_key
        if not api_key:
            raise RuntimeError("GROQ_API_KEY missing")
        model = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"model": model, "messages": req.messages,
                   "temperature": req.temperature, "max_tokens": req.max_tokens}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post("https://api.groq.com/openai/v1/chat/completions",
                                  json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return ChatResponse(text, Cost(usd=0.0))
