import cv2
import os


def _try_writer(output_path: str, fps: float, size: tuple) -> cv2.VideoWriter:
    """
    Try H.264 (avc1) first — browser-compatible.
    Fall back to mp4v if not available.
    """
    for fourcc_code in ("avc1", "H264", "X264", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*fourcc_code)
        writer = cv2.VideoWriter(output_path, fourcc, fps, size)
        if writer.isOpened():
            return writer
        writer.release()
    raise RuntimeError("No suitable video codec found (tried avc1, H264, X264, mp4v)")


def compress_video(input_path: str, output_path: str, skip_frames: int = 1):
    """
    Educational video compression using Frame Sampling + resolution halving.
    Writes browser-compatible H.264 MP4.
    Preserves audio using moviepy.
    """
    import tempfile
    import shutil
    import os
    from moviepy import VideoFileClip

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    new_fps    = max(1.0, fps / (skip_frames + 1))
    new_width  = max(2, int(width  / 2))
    new_height = max(2, int(height / 2))

    fd, temp_video = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)

    out = _try_writer(temp_video, new_fps, (new_width, new_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % (skip_frames + 1) == 0:
            resized = cv2.resize(frame, (new_width, new_height))
            out.write(resized)
        frame_count += 1

    cap.release()
    out.release()

    # Mux audio
    try:
        orig_clip = VideoFileClip(input_path)
        if orig_clip.audio is not None:
            new_clip = VideoFileClip(temp_video)
            # Match audio duration to new video duration
            audio = orig_clip.audio.with_duration(new_clip.duration)
            final_clip = new_clip.with_audio(audio)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
            final_clip.close()
            new_clip.close()
        else:
            shutil.copy(temp_video, output_path)
        orig_clip.close()
    except Exception as e:
        print(f"Warning: Audio muxing failed: {e}")
        shutil.copy(temp_video, output_path)
    finally:
        if os.path.exists(temp_video):
            try:
                os.remove(temp_video)
            except Exception:
                pass


def decompress_video(input_path: str, output_path: str, duplicate_frames: int = 1):
    """
    Educational video decompression: duplicate frames + double resolution.
    Writes browser-compatible H.264 MP4.
    Preserves audio using moviepy.
    """
    import tempfile
    import shutil
    import os
    from moviepy import VideoFileClip

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    new_fps    = min(fps * (duplicate_frames + 1), 120.0)
    new_width  = width  * 2
    new_height = height * 2

    fd, temp_video = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)

    out = _try_writer(temp_video, new_fps, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        restored = cv2.resize(frame, (new_width, new_height))
        for _ in range(duplicate_frames + 1):
            out.write(restored)

    cap.release()
    out.release()

    # Mux audio
    try:
        orig_clip = VideoFileClip(input_path)
        if orig_clip.audio is not None:
            new_clip = VideoFileClip(temp_video)
            audio = orig_clip.audio.with_duration(new_clip.duration)
            final_clip = new_clip.with_audio(audio)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
            final_clip.close()
            new_clip.close()
        else:
            shutil.copy(temp_video, output_path)
        orig_clip.close()
    except Exception as e:
        print(f"Warning: Audio muxing failed: {e}")
        shutil.copy(temp_video, output_path)
    finally:
        if os.path.exists(temp_video):
            try:
                os.remove(temp_video)
            except Exception:
                pass


def compression_ratio(original_size: int, processed_size: int) -> float:
    if original_size == 0:
        return 0.0
    return round(((original_size - processed_size) / original_size) * 100, 2)
