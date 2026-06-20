import os
import re
import uuid

TMP_DIR = "tmp"


def init_tmp():
    os.makedirs(TMP_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Remove / replace characters that are illegal in Windows/Linux file paths.
    Keeps only alphanumerics, dots, underscores, and hyphens.
    """
    # Separate name and extension
    name, ext = os.path.splitext(filename)

    # Replace any character that is not word-char, hyphen, or space → underscore
    name = re.sub(r'[^\w\s\-]', '_', name)   # remove special chars
    name = re.sub(r'[\s/\\:*?"<>|]+', '_', name)  # replace path seps & spaces
    name = re.sub(r'_+', '_', name)           # collapse consecutive underscores
    name = name.strip('_')

    # Keep extension clean too (just the dot + alphanumeric)
    ext = re.sub(r'[^a-zA-Z0-9.]', '', ext)

    return name + ext


def save_temp_file(filename: str, content: bytes) -> str:
    init_tmp()

    safe_name  = sanitize_filename(filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"

    path = os.path.join(TMP_DIR, unique_name)

    with open(path, "wb") as f:
        f.write(content)

    return path