from pydantic import BaseModel
from typing import Optional

class ProcessResponse(BaseModel):
    status: str
    media_type: str
    original_size: int
    processed_size: int
    compression_ratio: float
    processing_time_ms: int
    message: str | None = None
    download_url: str | None = None
    psnr: Optional[float] = None
    mse: Optional[float] = None