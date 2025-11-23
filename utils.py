
# utils.py
import re
from datetime import datetime

def clean_text(text: str) -> str:
    """Remove extra spaces and line breaks."""
    return re.sub(r'\s+', ' ', text).strip()

def format_title(title: str) -> str:
    """Ensure section titles are standardized."""
    return title.strip().title()

def timestamp():
    """Return current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def extract_company_name(text: str) -> str | None:
    """Try to extract a company name from user text."""
    match = re.search(r"\bfor ([A-Za-z0-9 .&-]+)", text.lower())
    if match:
        return match.group(1).strip().title()
    return None

