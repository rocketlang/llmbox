import httpx
from .base import Provider, ChatRequest, ChatResponse
from ..utils.cost import Cost
from ..utils.config import SETTINGS

class OpenRouterProvider(Provider):
    name = "openrouter"
    free_tier = False

    async def chat(self, req: ChatRequest) -> ChatResponse:
        key = SETTINGS.openrouter_api_key
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY missing")
        headers = {"Authorization": f"Bearer {key}"}
        payload = {"model":"anthropic/claude-3.5-sonnet","messages":req.messages}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{SETTINGS.openrouter_base_url}/chat/completions",
                                  json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return ChatResponse(text, Cost(usd=0.01))
