from .base import Provider, ChatRequest, ChatResponse
from ..utils.cost import Cost
from ..utils.config import SETTINGS
import httpx

class OllamaProvider(Provider):
    name = "ollama"
    free_tier = True

    async def chat(self, req: ChatRequest) -> ChatResponse:
        base = SETTINGS.ollama_base_url or ""
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                await client.get(f"{base}/api/tags")
        except Exception as e:
            raise RuntimeError(f"Ollama unreachable: {e}")
        return ChatResponse("Ollama local inference not wired yet.", Cost(usd=0.0))
