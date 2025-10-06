from langdetect import detect

INDIC = {"hi","ta","te","bn","ml","kn","mr","gu"}
def detect_lang(text: str) -> str:
    try:
        return detect(text)  # ISO 639-1
    except Exception:
        return "en"

def is_indic(lang: str) -> bool:
    return lang in INDIC
