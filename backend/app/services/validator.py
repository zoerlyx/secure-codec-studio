import os

# ── Supported extensions ────────────────────────────────────────────────────────
IMAGE_EXT = [".png", ".jpg", ".jpeg", ".bmp", ".webp"]
AUDIO_EXT = [".wav", ".mp3", ".ogg", ".m4a", ".aac", ".mpeg", ".flac"]
VIDEO_EXT = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

# Legacy extensions (treated as their parent type)
RLE_EXT   = [".rle"]
DELTA_EXT = [".delta"]

# ── File size limits ────────────────────────────────────────────────────────────
LIMITS = {
    "image":  30 * 1024 * 1024,   # 30 MB
    "audio":  50 * 1024 * 1024,   # 50 MB
    "video": 150 * 1024 * 1024,   # 150 MB
}

# ── Audio formats that need conversion to WAV before processing ─────────────────
NON_WAV_AUDIO = [".mp3", ".ogg", ".m4a", ".aac", ".mpeg", ".flac"]


def detect_media(filename: str) -> str:
    parts = filename.split('.')
    if len(parts) < 2:
        return None
    
    ext = f".{parts[-1]}".lower()

    if ext == '.lossless':
        if len(parts) >= 3:
            real_ext = f".{parts[-2]}".lower()
            ext = real_ext
        else:
            base = parts[0].lower()
            for known in IMAGE_EXT + AUDIO_EXT + VIDEO_EXT:
                if base.endswith(f"_{known[1:]}"):
                    ext = known
                    break

    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in VIDEO_EXT:
        return "video"

    return None

def validate_size(media_type: str, size: int, mode: str = None):
    if media_type is None:
        raise ValueError(
            "Unsupported file type. "
            "Supported: PNG/JPG/BMP/WebP (image), WAV/MP3/OGG/M4A/AAC/FLAC (audio), MP4/AVI/MOV/MKV (video)."
        )

    limit = LIMITS[media_type]
    
    # Increase limit massively (2 GB) for video extraction because uncompressed AVI stego files are huge
    if media_type == "video" and mode == "extract":
        limit = 2000 * 1024 * 1024

    if size > limit:
        limit_mb = limit // (1024 * 1024)
        raise ValueError(f"File size exceeded limit ({limit_mb} MB for {media_type}).")


def needs_audio_conversion(path: str) -> bool:
    """Return True if the audio file needs to be converted to WAV first."""
    ext = os.path.splitext(path)[1].lower()
    return ext in NON_WAV_AUDIO