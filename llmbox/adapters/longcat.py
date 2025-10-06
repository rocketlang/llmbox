import httpx
from .base import Provider, ChatRequest, ChatResponse
from ..utils.cost import Cost
from ..utils.config import SETTINGS

class LongCatProvider(Provider):
    name = "longcat"
    free_tier = True

    async def chat(self, req: ChatRequest) -> ChatResponse:
        key = SETTINGS.longcat_api_key
        if not key:
            raise RuntimeError("LONGCAT_API_KEY missing")
        headers = {"Authorization": f"Bearer {key}"}
        payload = {"model":"LongCat-Flash-Chat","messages":req.messages}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post("https://api.longcat.chat/openai/chat/completions",
                                  json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return ChatResponse(text, Cost(usd=0.0))
