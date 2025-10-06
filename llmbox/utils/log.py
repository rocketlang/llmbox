from os import getenv
from rich.console import Console

_console = Console()
_DEBUG = getenv("LLMBOX_DEBUG","").lower() in ("1","true","yes","y","on")

def _print(prefix, style, msg):
    if not _DEBUG:  # print only when debug enabled
        return
    _console.print(f"{prefix} [bold {style}]{msg}[/]")

def info(msg): _print("🧠", "blue", msg)
def ok(msg):   _print("✅", "green", msg)
def warn(msg): _print("⚠️", "yellow", msg)
def err(msg):  _print("❌", "red", msg)
