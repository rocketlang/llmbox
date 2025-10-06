from llmbox.router.core import LLMBox

def test_can_instantiate():
    r = LLMBox.chat("Hello")
    assert isinstance(r.content, str)
