import re
import uuid
from datetime import datetime
from pathlib import Path
from app.core.settings import settings

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")

def sanitize_filename(name: str) -> str:
    name = Path(name).name.strip()
    if not name:
        name = "file"
    safe = _SAFE_CHARS.sub("-", name)
    safe = re.sub(r"\.{2,}", ".", safe).strip(".")
    
    return safe or "file"

def validate_content_type(ct: str) -> str:
    allowed = {c.strip() for c in settings.ALLOWED_CONTENT_TYPES.split(",") if c.strip()}
    if ct not in allowed:
        raise ValueError(f"content_type '{ct}' not allowed")
    
    return ct

def build_object_key(original_filename: str) -> str:
    today = datetime.utcnow()
    safe = sanitize_filename(original_filename)
    uid = uuid.uuid4().hex
    date_prefix = f"{today:%Y/%m/%d}"
    prefix = settings.S3_PREFIX.rstrip("/") + "/" if settings.S3_PREFIX else ""
    
    return f"{prefix}{date_prefix}/{uid}__{safe}"
