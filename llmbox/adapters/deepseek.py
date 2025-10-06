import httpx
from .base import Provider, ChatRequest, ChatResponse
from ..utils.cost import Cost
from ..utils.config import SETTINGS

class DeepSeekProvider(Provider):
    name = "deepseek"
    free_tier = False

    async def chat(self, req: ChatRequest) -> ChatResponse:
        key = SETTINGS.deepseek_api_key
        if not key:
            raise RuntimeError("DEEPSEEK_API_KEY missing")
        headers = {"Authorization": f"Bearer {key}"}
        payload = {"model":"deepseek-chat","messages":req.messages}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post("https://api.deepseek.com/chat/completions",
                                  json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            # rough placeholder cost
            return ChatResponse(text, Cost(usd=0.001))
