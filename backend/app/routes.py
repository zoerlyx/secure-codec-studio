import os
import time

from fastapi import APIRouter, UploadFile, File, Form, Request, Query
from fastapi.responses import JSONResponse, StreamingResponse, Response
from fastapi.exceptions import HTTPException

from app.services.image_service import process_image
from app.services.audio_service import process_audio
from app.services.video_service import process_video
from app.schemas import ProcessResponse
from app.utils import save_temp_file
from app.services.validator import detect_media, validate_size

router = APIRouter()

TMP_DIR = os.path.join(os.getcwd(), "tmp")

@router.post("/process", response_model=ProcessResponse)
async def process_file(
    request: Request,
    file: UploadFile = File(...),
    mode: str = Form(...),
    compress_type: str = Form("lossy"),
    message: str = Form(None)
):
    try:
        start = time.time()
        content = await file.read()
        
        media_type = detect_media(file.filename)
        validate_size(media_type, len(content), mode)

        temp_path = save_temp_file(file.filename, content)

        if media_type == "image":
            result = process_image(temp_path, mode, compress_type, message)
        elif media_type == "audio":
            result = process_audio(temp_path, mode, compress_type, message)
        elif media_type == "video":
            result = process_video(temp_path, mode, compress_type, message)
        else:
            raise ValueError(f"Unsupported media type: {media_type}")

        download_url = None
        if result.get("output_path") and os.path.exists(result["output_path"]):
            filename = os.path.basename(result["output_path"])
            download_url = f"/download/{filename}"

        return ProcessResponse(
            status=result["status"],
            media_type=result["media_type"],
            original_size=result["original_size"],
            processed_size=result["processed_size"],
            compression_ratio=result["compression_ratio"],
            processing_time_ms=result["processing_time_ms"],
            message=result["message"],
            download_url=download_url,
            psnr=result.get("psnr"),
            mse=result.get("mse"),
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


# ─── MIME types for served files ───────────────────────────────────────────────
MEDIA_MIME = {
    ".mp4":  "video/mp4",
    ".avi":  "video/x-msvideo",
    ".mov":  "video/quicktime",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".bmp":  "image/bmp",
    ".wav":  "audio/wav",
    ".mp3":  "audio/mpeg",
}

@router.get("/download/{filename}")
async def download_file(filename: str, request: Request, preview: bool = False, download: bool = False):
    """
    Serve files with full HTTP Range request support.
    """
    temp_dir = os.path.join(os.getcwd(), "tmp")
    file_path = os.path.join(temp_dir, filename)

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"message": "File not found"})
        
    if preview and filename.endswith(".lossless"):
        from app.algorithms.lossless.zlib_codec import decompress_lossless
        parts = filename.split('.')
        real_ext = f".{parts[-2]}"
        temp_preview_path = os.path.join(temp_dir, f"preview_{parts[0]}{real_ext}")
        try:
            decompress_lossless(file_path, temp_preview_path)
            file_path = temp_preview_path
            filename = os.path.basename(temp_preview_path)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Failed to preview lossless file: {e}"})

    ext = os.path.splitext(filename)[1].lower()
    content_type = MEDIA_MIME.get(ext, "application/octet-stream")
    file_size = os.path.getsize(file_path)
    
    disposition = "attachment" if download else "inline"

    range_header = request.headers.get("range")
    if range_header:
        try:
            range_val = range_header.replace("bytes=", "").strip()
            parts = range_val.split("-")
            start = int(parts[0]) if parts[0] else 0
            end   = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
        except Exception:
            start, end = 0, file_size - 1

        end = min(end, file_size - 1)
        chunk_size = end - start + 1

        def iter_chunk(path: str, s: int, length: int):
            with open(path, "rb") as f:
                f.seek(s)
                remaining = length
                while remaining > 0:
                    data = f.read(min(65536, remaining))
                    if not data: break
                    remaining -= len(data)
                    yield data

        headers = {
            "Content-Range":       f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges":       "bytes",
            "Content-Length":      str(chunk_size),
            "Content-Disposition": f'{disposition}; filename="{filename}"',
            "Cache-Control":       "no-cache",
        }
        return StreamingResponse(
            iter_chunk(file_path, start, chunk_size),
            status_code=206,
            headers=headers,
            media_type=content_type,
        )

    def iter_full(path: str):
        with open(path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk: break
                yield chunk

    headers = {
        "Accept-Ranges":       "bytes",
        "Content-Length":      str(file_size),
        "Content-Disposition": f'{disposition}; filename="{filename}"',
        "Cache-Control":       "no-cache",
    }
    return StreamingResponse(
        iter_full(file_path),
        status_code=200,
        headers=headers,
        media_type=content_type,
    )