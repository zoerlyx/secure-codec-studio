import os
import time

from app.algorithms.audio.downsample import (
    compress_audio_downsample,
    decompress_audio_upsample
)

from app.algorithms.metrics import calculate_audio_psnr, calculate_audio_mse

from app.algorithms.audio.lsb import (
    encode_lsb,
    decode_lsb,
)

from app.services.validator import needs_audio_conversion


# ── Audio conversion helper ─────────────────────────────────────────────────────

def _to_wav(path: str) -> str:
    """
    Convert any audio format to a WAV file using moviepy.
    Returns the WAV path (either the original if already WAV, or a new converted file).
    """
    if not needs_audio_conversion(path):
        return path

    wav_path = os.path.splitext(path)[0] + "_converted.wav"

    try:
        from moviepy import AudioFileClip
        clip = AudioFileClip(path)
        clip.write_audiofile(wav_path, logger=None)
        clip.close()
        return wav_path
    except Exception as e:
        raise ValueError(
            f"Cannot process this audio format. "
            f"Please convert to WAV and try again. (Details: {e})"
        )


# ── Public API ──────────────────────────────────────────────────────────────────

def process_audio(path: str, mode: str, compress_type: str = "lossy", message: str = None):
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
        msg = "Audio compressed losslessly using Zlib"
    else:
        wav_path = _to_wav(path)
        temp_wav = os.path.join(os.path.dirname(path), f"{filename}_temp_compressed.wav")
        compress_audio_downsample(wav_path, temp_wav)
        
        psnr = calculate_audio_psnr(wav_path, temp_wav)
        mse  = calculate_audio_mse(wav_path, temp_wav)
        
        if ext.lower() in [".mp3", ".ogg", ".m4a", ".aac", ".flac"]:
            output_path = os.path.join(os.path.dirname(path), f"{filename}_compressed.mp3")
            try:
                from moviepy import AudioFileClip
                clip = AudioFileClip(temp_wav)
                clip.write_audiofile(output_path, logger=None, bitrate="32k")
                clip.close()
                msg = "Audio compressed (Downsampling + MP3 32k Re-encoding)"
            except Exception as e:
                output_path = temp_wav
                msg = f"Audio compressed using Downsampling (Lossy) - MP3 conversion failed: {e}"
            finally:
                if output_path != temp_wav and os.path.exists(temp_wav):
                    try: os.remove(temp_wav)
                    except: pass
        else:
            output_path = os.path.join(os.path.dirname(path), f"{filename}_compressed.wav")
            import shutil
            shutil.move(temp_wav, output_path)
            msg = "Audio compressed using Downsampling (Lossy)"

    original_size = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "audio",
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
        real_ext = f".{parts[-2]}" if len(parts) >= 3 else ".wav"
        output_path = os.path.join(os.path.dirname(path), f"{filename}_restored{real_ext}")
        from app.algorithms.lossless.zlib_codec import decompress_lossless
        decompress_lossless(path, output_path)
        msg = "Audio restored perfectly (Lossless)"
    else:
        raise ValueError(
            "File ini adalah hasil kompresi Lossy (atau file original). "
            "Data yang dibuang oleh kompresi Lossy hilang secara permanen dan tidak dapat di-restore. "
            "Harap unggah file hasil kompresi Lossless (.lossless) untuk melakukan dekompresi."
        )

    original_size  = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "audio",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": round(((processed_size - original_size) / original_size) * 100, 2) if original_size > 0 else 0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": msg,
        "output_path": output_path,
    }


def stego(path, message):

    if not message:
        raise ValueError("Message is required")

    start = time.time()

    # LSB steganography requires WAV
    wav_path = _to_wav(path)

    filename = os.path.splitext(os.path.basename(path))[0]
    output_path = os.path.join(
        os.path.dirname(path),
        f"{filename}_stego.wav"
    )

    encode_lsb(wav_path, output_path, message)

    original_size  = os.path.getsize(path)
    processed_size = os.path.getsize(output_path)

    return {
        "status": "success",
        "media_type": "audio",
        "original_size": original_size,
        "processed_size": processed_size,
        "compression_ratio": round(((processed_size - original_size) / original_size) * 100, 2) if original_size > 0 else 0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": "Hidden message embedded successfully",
        "output_path": output_path,
    }


def extract(path):
    start = time.time()

    wav_path = _to_wav(path)
    message  = decode_lsb(wav_path)

    original_size = os.path.getsize(path)

    return {
        "status": "success",
        "media_type": "audio",
        "original_size": original_size,
        "processed_size": original_size,
        "compression_ratio": 0.0,
        "processing_time_ms": int((time.time() - start) * 1000),
        "message": message,
        "output_path": None,
    }