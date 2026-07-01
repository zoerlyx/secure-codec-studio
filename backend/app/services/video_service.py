import os
import time

from app.algorithms.video.compression import (
    compress_video,
    decompress_video,
    compression_ratio
)

from app.algorithms.video.lsb import (
    encode_lsb,
    decode_lsb
)

from app.algorithms.metrics import calculate_video_psnr, calculate_video_mse

def process_video(path: str, mode: str, compress_type: str = "lossy", message: str = None):
    if mode == "compress":
        return compress(path, compress_type)
    elif mode == "decompress":
        return decompress(path)
    elif mode == "stego":
        return stego(path, message)
    elif mode == "extract":
        return extract(path)
    raise ValueError("Unknown mode")


def compress(path: str, compress_type: str):
    start = time.time()
    filename = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(path)[1]
    
    if compress_type == "lossless":
        output_path = os.path.join(os.path.dirname(path), f"{filename}_compressed{ext}.lossless")
        from app.algorithms.lossless.zlib_codec import compress_lossless
        compress_lossless(path, output_path)
        psnr = float('inf')
        mse = 0.0
        msg = "Video compressed losslessly using Zlib"
    else:
        output_path = os.path.join(os.path.dirname(path), f"{filename}_compressed.mp4")
        compress_video(path, output_path)
        psnr = calculate_video_psnr(path, output_path)
        mse = calculate_video_mse(path, output_path)
        msg = "Video compressed using Frame Dropping & Resizing (Lossy)"

    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "video",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": round(((original_size - processed_size) / original_size) * 100, 2) if original_size > 0 else 0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": msg,
        "output_path": output_path,
        "psnr": psnr,
        "mse": mse
    }


def decompress(path: str):
    start = time.time()
    
    parts = os.path.basename(path).split('.')
    if path.lower().endswith(".lossless"):
        filename = parts[0]
        real_ext = f".{parts[-2]}" if len(parts) >= 3 else ".mp4"
        output_path = os.path.join(os.path.dirname(path), f"{filename}_restored{real_ext}")
        from app.algorithms.lossless.zlib_codec import decompress_lossless
        decompress_lossless(path, output_path)
        msg = "Video restored perfectly (Lossless)"
    else:
        raise ValueError(
            "File ini adalah hasil kompresi Lossy (atau file original). "
            "Data yang dibuang oleh kompresi Lossy hilang secara permanen dan tidak dapat di-restore. "
            "Harap unggah file hasil kompresi Lossless (.lossless) untuk melakukan dekompresi."
        )

    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "video",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": round(((processed_size - original_size) / original_size) * 100, 2) if original_size > 0 else 0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": msg,
        "output_path": output_path
    }


def stego(path, message):
    if not message:
        raise ValueError("Message is required")

    start = time.time()

    filename = os.path.splitext(os.path.basename(path))[0]
    # Using .avi for uncompressed output to preserve LSBs
    output_path = os.path.join(
        os.path.dirname(path),
        f"{filename}_stego.avi"
    )

    encode_lsb(path, output_path, message)

    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "video",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": compression_ratio(
            original_size,
            processed_size
        ),
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": "Hidden message embedded successfully",
        "output_path": output_path
    }


def extract(path):
    start = time.time()

    message = decode_lsb(path)

    original_size = os.path.getsize(path)

    return {
        "status": "success",
        "media_type": "video",
        "original_size": original_size,
        "processed_size": original_size,
        "compression_ratio": 1.0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": message,
        "output_path": None
    }
