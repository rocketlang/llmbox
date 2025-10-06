from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..utils.cost import Cost

@dataclass
class ChatRequest:
    messages: list[dict]
    max_tokens: int | None = None
    temperature: float = 0.7

@dataclass
class ChatResponse:
    content: str
    cost: Cost

class Provider(ABC):
    name: str
    free_tier: bool = False
    languages: set[str] = set()  # "all" if empty

    @abstractmethod
    async def chat(self, req: ChatRequest) -> ChatResponse: ...
