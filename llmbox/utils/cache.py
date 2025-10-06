import os, sqlite3, time, hashlib, json, threading
from pathlib import Path

CACHE_DIR = Path(os.getenv("LLMBOX_CACHE_DIR", str(Path.home()/".llmbox")))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CACHE_DIR / "cache.db"
TTL = int(os.getenv("LLMBOX_CACHE_TTL_SECS", "21600"))  # 6h

_lock = threading.Lock()

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS cache (
        k TEXT PRIMARY KEY,
        v TEXT NOT NULL,
        ts INTEGER NOT NULL
    )""")
    return conn

def _key(lang: str, provider: str, req: dict) -> str:
    payload = {"lang":lang, "provider":provider, **req}
    s = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def get(lang: str, provider: str, req: dict):
    k = _key(lang, provider, req)
    with _lock, _connect() as conn:
        cur = conn.execute("SELECT v, ts FROM cache WHERE k=?", (k,))
        row = cur.fetchone()
        if not row: return None
        v, ts = row
        if time.time() - ts > TTL:
            conn.execute("DELETE FROM cache WHERE k=?", (k,))
            return None
        try:
            return json.loads(v)
        except Exception:
            return None

def set(lang: str, provider: str, req: dict, value: dict):
    k = _key(lang, provider, req)
    payload = json.dumps(value, ensure_ascii=False)
    with _lock, _connect() as conn:
        conn.execute("REPLACE INTO cache (k,v,ts) VALUES (?,?,?)",
                     (k, payload, int(time.time())))
