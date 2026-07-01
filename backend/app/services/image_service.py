import os
import time

from app.algorithms.image.kmeans import (
    compress_image_kmeans,
    decompress_image_kmeans
)
from app.algorithms.image.lsb import encode_lsb, decode_lsb
from app.algorithms.metrics import calculate_psnr, calculate_mse

def process_image(path: str, mode: str, compress_type: str = "lossy", message: str = None):
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
        msg = "Image compressed losslessly using Zlib"
    else:
        output_path = os.path.join(os.path.dirname(path), f"{filename}_compressed.jpg")
        compress_image_kmeans(path, output_path, k=128)
        psnr = calculate_psnr(path, output_path)
        mse = calculate_mse(path, output_path)
        msg = "Image compressed using K-Means Quantization (Lossy)"

    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "image",
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
        real_ext = f".{parts[-2]}" if len(parts) >= 3 else ".png"
        output_path = os.path.join(os.path.dirname(path), f"{filename}_restored{real_ext}")
        from app.algorithms.lossless.zlib_codec import decompress_lossless
        decompress_lossless(path, output_path)
        msg = "Image restored perfectly (Lossless)"
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
        "media_type": "image",
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
    output_path = os.path.join(os.path.dirname(path), f"{filename}_stego.png")
    encode_lsb(path, output_path, message)
    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)
    return {
        "status": "success",
        "media_type": "image",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": round(((processed_size - original_size) / original_size) * 100, 2) if original_size > 0 else 0,
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
        "media_type": "image",
        "original_size": original_size,
        "processed_size": original_size,
        "compression_ratio": 1.0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": message,
        "output_path": None
    }