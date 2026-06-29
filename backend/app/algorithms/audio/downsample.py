import wave
import struct

def compress_audio_downsample(input_path: str, output_path: str):
    """
    Compress audio by halving the sample rate (downsampling)
    and halving the number of channels (to mono if stereo).
    """
    with wave.open(input_path, 'rb') as wav_in:
        n_channels = wav_in.getnchannels()
        sampwidth = wav_in.getsampwidth()
        framerate = wav_in.getframerate()
        n_frames = wav_in.getnframes()
        
        frames = wav_in.readframes(n_frames)
        
    # Unpack based on sample width
    if sampwidth == 1:
        fmt = f"{n_frames * n_channels}B"
    elif sampwidth == 2:
        fmt = f"<{n_frames * n_channels}h"
    else:
        raise ValueError("Unsupported sample width")
        
    samples = struct.unpack(fmt, frames)
    
    # If stereo, convert to mono by taking average
    if n_channels == 2:
        samples = [(samples[i] + samples[i+1]) // 2 for i in range(0, len(samples), 2)]
        new_channels = 1
    else:
        new_channels = n_channels
        
    # Downsample by taking every 2nd sample
    samples_down = samples[::2]
    new_framerate = framerate // 2
    
    # Pack back
    if sampwidth == 1:
        new_fmt = f"{len(samples_down)}B"
    else:
        new_fmt = f"<{len(samples_down)}h"
        
    new_frames = struct.pack(new_fmt, *samples_down)
    
    with wave.open(output_path, 'wb') as wav_out:
        wav_out.setnchannels(new_channels)
        wav_out.setsampwidth(sampwidth)
        wav_out.setframerate(new_framerate)
        wav_out.writeframes(new_frames)


def decompress_audio_upsample(input_path: str, output_path: str):
    """
    Decompression for downsampled audio just restores the sample rate metadata 
    or interpolates. For MVP, we just copy or duplicate samples.
    """
    with wave.open(input_path, 'rb') as wav_in:
        n_channels = wav_in.getnchannels()
        sampwidth = wav_in.getsampwidth()
        framerate = wav_in.getframerate()
        n_frames = wav_in.getnframes()
        
        frames = wav_in.readframes(n_frames)
        
    if sampwidth == 1:
        fmt = f"{n_frames * n_channels}B"
    elif sampwidth == 2:
        fmt = f"<{n_frames * n_channels}h"
    else:
        raise ValueError("Unsupported sample width")
        
    samples = struct.unpack(fmt, frames)
    
    # Duplicate samples to upsample
    samples_up = []
    for s in samples:
        samples_up.extend([s, s])
        
    new_framerate = framerate * 2
    
    if sampwidth == 1:
        new_fmt = f"{len(samples_up)}B"
    else:
        new_fmt = f"<{len(samples_up)}h"
        
    new_frames = struct.pack(new_fmt, *samples_up)
    
    with wave.open(output_path, 'wb') as wav_out:
        wav_out.setnchannels(n_channels)
        wav_out.setsampwidth(sampwidth)
        wav_out.setframerate(new_framerate)
        wav_out.writeframes(new_frames)
