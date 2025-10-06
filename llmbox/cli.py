import asyncio
import os
import typer
from dotenv import load_dotenv; load_dotenv()
from llmbox.router.core import LLMBox

app = typer.Typer(help="LLMBox CLI - universal LLM router")

@app.command()
def chat(text: str, provider: str = typer.Option(None), max_tokens: int = typer.Option(None)):
    """Run a one-shot chat request"""
    async def _run():
        resp = await LLMBox.a_chat(text, provider=provider, max_tokens=max_tokens)
        typer.echo(resp.content)
    asyncio.run(_run())

@app.command()
def serve(port: int = 8080, host: str = "0.0.0.0"):
    """Run the LLMBox FastAPI server"""
    from llmbox.server.api import api
    import uvicorn
    uvicorn.run(api, host=host, port=port, reload=bool(os.getenv("DEV", "")))

if __name__ == "__main__":
    app()
