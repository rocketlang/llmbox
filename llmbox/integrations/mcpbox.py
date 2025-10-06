import httpx
from ..utils.config import SETTINGS

async def ping_mcpbox() -> bool:
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{SETTINGS.mcpbox_base_url}/health",
                            headers={"Authorization": f"Bearer {SETTINGS.mcpbox_token or ''}"})
            return r.status_code == 200
    except Exception:
        return False
