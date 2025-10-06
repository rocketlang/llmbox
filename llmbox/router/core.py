import asyncio, os
from typing import Optional
from ..utils.config import SETTINGS
from ..utils.language import detect_lang, is_indic
from ..utils.cost import Cost
from ..utils.cache import get as cache_get, set as cache_set
from ..utils.log import info, ok, warn, err
from ..adapters.base import ChatRequest, ChatResponse, Provider
from ..adapters.groq import GroqProvider
from ..adapters.ollama import OllamaProvider
from ..adapters.longcat import LongCatProvider
from ..adapters.deepseek import DeepSeekProvider
from ..adapters.openrouter import OpenRouterProvider

PROVIDERS: dict[str, Provider] = {
    "groq": GroqProvider(),
    "ollama": OllamaProvider(),
    "longcat": LongCatProvider(),
    "deepseek": DeepSeekProvider(),
    "openrouter": OpenRouterProvider(),
}

def _ordered_providers(lang: str) -> list[str]:
    order = list(SETTINGS.fallback_providers)
    if is_indic(lang) and "longcat" in order:
        # Prefer LongCat for Indic
        order.remove("longcat"); order.insert(0, "longcat")
    return order

class LLMBox:
    @staticmethod
    def conversation():
        return Conversation()

    @staticmethod
    def _pick_first_available(order: list[str]) -> list[Provider]:
        return [PROVIDERS[p] for p in order if p in PROVIDERS]

    @staticmethod
    async def a_chat(text: str, provider: Optional[str]=None, max_tokens: Optional[int]=None, temperature: float=0.7) -> ChatResponse:
        lang = detect_lang(text) if SETTINGS.lang_mode == "auto" else "en"
        req = ChatRequest(messages=[{"role":"user","content":text}],
                          max_tokens=max_tokens, temperature=temperature)

        order = [provider] if provider else _ordered_providers(lang)
        info(f"lang={lang} order={order}")

        # Cache check (per provider attempt)
        base_req = {"messages": req.messages, "max_tokens": req.max_tokens, "temperature": req.temperature}

        last_err = None
        for name in order:
            prov = PROVIDERS.get(name)
            if not prov: 
                warn(f"provider not found: {name}")
                continue

            cached = cache_get(lang, name, base_req)
            if cached:
                ok(f"cache hit → {name}")
                return ChatResponse(cached["content"], Cost(**cached.get("cost", {"usd":0.0})))

            try:
                info(f"routing → {name}")
                resp = await prov.chat(req)
                ok(f"success ← {name}")
                cache_set(lang, name, base_req, {"content": resp.content, "cost": resp.cost.__dict__})
                if resp.cost.usd <= SETTINGS.max_cost_per_request:
                    return resp
                else:
                    warn(f"cost {resp.cost.usd} exceeded max {SETTINGS.max_cost_per_request}; continuing")
            except Exception as e:
                warn(f"failed {name}: {e}")
                last_err = e
                continue

        if last_err:
            err(f"All providers failed. Last error: {last_err}")
        return ChatResponse("All providers failed.", Cost())

class Conversation:
    def __init__(self):
        self.messages: list[dict] = []
        self.cost = Cost()

    def add(self, text: str):
        self.messages.append({"role":"user","content":text})
        r = asyncio.get_event_loop().run_until_complete(LLMBox.a_chat(text))
        self.cost.add(r.cost)
        self.messages.append({"role":"assistant","content":r.content})
        return r.content
