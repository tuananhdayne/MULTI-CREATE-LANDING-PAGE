import re
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings


def clean_markdown_code(raw_text: str) -> str:
    """
    Cleans and extracts raw HTML5 code from LLM responses that may be
    wrapped in markdown code blocks (` ```html ... ``` `) or surrounded by conversational text.
    """
    if not raw_text:
        return ""

    text = raw_text.strip()

    # Pattern 1: Match ```html ... ``` or ```xml ... ``` or ``` ... ```
    code_block_match = re.search(r"```(?:html|xml)?\s*\n([\s\S]*?)\n```", text, re.IGNORECASE)
    if code_block_match:
        extracted = code_block_match.group(1).strip()
        # Further verify if it has HTML structure
        if "<html" in extracted.lower() or "<!doctype" in extracted.lower():
            return extracted

    # Pattern 2: Search for <!DOCTYPE html> ... </html>
    html_doc_match = re.search(r"(<!DOCTYPE\s+html[\s\S]*?</html>)", text, re.IGNORECASE)
    if html_doc_match:
        return html_doc_match.group(1).strip()

    # Pattern 3: Search for <html ... </html>
    html_tag_match = re.search(r"(<html[\s\S]*?</html>)", text, re.IGNORECASE)
    if html_tag_match:
        return html_tag_match.group(1).strip()

    # Fallback: Strip leading/trailing backticks if any
    if text.startswith("```") and text.endswith("```"):
        lines = text.split("\n")
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()

    return text


def get_gemini_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7
) -> ChatGoogleGenerativeAI:
    """
    Instantiates an authenticated Google Gemini LLM instance via LangChain.
    Strictly safeguards API keys from exposure.
    """
    settings = get_settings()
    selected_model = model_name or settings.gemini_model or "gemini-2.5-flash"
    api_key = settings.gemini_api_key

    # Initialize ChatGoogleGenerativeAI with secret key
    return ChatGoogleGenerativeAI(
        model=selected_model,
        google_api_key=api_key or "DUMMY_KEY_FOR_TESTING",
        temperature=temperature,
        timeout=120,
        max_retries=2,
    )
