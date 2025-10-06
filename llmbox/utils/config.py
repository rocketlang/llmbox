from dataclasses import dataclass
import os

# ✅ Always load .env first (from project root by default)
try:
    from dotenv import load_dotenv
    load_dotenv()   # loads .env into process env
except Exception:
    pass

def _bool(v: str | None, default=False) -> bool:
    if v is None: return default
    return v.lower() in ("1","true","yes","y","on")

@dataclass(frozen=True)
class Settings:
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "groq")
    fallback_providers: tuple[str, ...] = tuple(os.getenv("FALLBACK_PROVIDERS", "groq,ollama").split(","))
    prefer_free_tier: bool = _bool(os.getenv("PREFER_FREE_TIER", "true"))
    max_cost_per_request: float = float(os.getenv("MAX_COST_PER_REQUEST", "0.01"))
    lang_mode: str = os.getenv("LLMBOX_LANG_MODE", "auto")

    # MCPBox
    mcpbox_base_url: str = os.getenv("MCPBOX_BASE_URL", "http://127.0.0.1:8711")
    mcpbox_token: str | None = os.getenv("MCPBOX_TOKEN")

    # Provider keys/urls
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    longcat_api_key: str | None = os.getenv("LONGCAT_API_KEY")
    deepseek_api_key: str | None = os.getenv("DEEPSEEK_API_KEY")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL","https://openrouter.ai/api/v1")

SETTINGS = Settings()
