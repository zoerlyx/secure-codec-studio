import struct
import wave
from typing import List


def delta_encode(samples: List[int]) -> bytes:
    """
    Encode 16-bit PCM samples using Delta Encoding.

    Output format:
        First Sample : int16 (2 bytes)
        Remaining    : int16 delta (2 bytes each)
    """

    if not samples:
        return b""

    encoded = bytearray()

    # Store first sample
    encoded.extend(struct.pack("<h", samples[0]))

    previous = samples[0]

    # Store remaining deltas
    for current in samples[1:]:

        delta = current - previous

        if delta < -32768 or delta > 32767:
            raise ValueError("Delta overflow")

        encoded.extend(struct.pack("<h", delta))

        previous = current

    return bytes(encoded)


def delta_decode(data: bytes) -> List[int]:
    """
    Decode Delta Encoding back into 16-bit PCM samples.
    """

    if not data:
        return []

    if len(data) < 2:
        raise ValueError("Invalid delta data")

    if (len(data) - 2) % 2 != 0:
        raise ValueError("Invalid delta data")

    first_sample = struct.unpack("<h", data[:2])[0]

    samples = [first_sample]

    previous = first_sample
    offset = 2

    while offset < len(data):

        delta = struct.unpack(
            "<h",
            data[offset:offset + 2]
        )[0]

        current = previous + delta

        if current < -32768 or current > 32767:
            raise ValueError("Invalid delta data")

        samples.append(current)

        previous = current
        offset += 2

    return samples


def compression_ratio(
    original_size: int,
    processed_size: int
) -> float:
    """
    Calculate compression ratio (%).
    """

    if original_size == 0:
        return 0.0

    return round(
        ((original_size - processed_size) / original_size) * 100,
        2
    )


def read_wav(path: str):
    """
    Read WAV PCM 16-bit little-endian.

    Returns:
        sample_rate,
        channels,
        samples
    """

    with wave.open(path, "rb") as wav:

        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frame_count = wav.getnframes()

        if sample_width != 2:
            raise ValueError(
                "Only 16-bit PCM WAV is supported."
            )

        raw_data = wav.readframes(frame_count)

    sample_count = len(raw_data) // 2

    samples = list(
        struct.unpack(
            f"<{sample_count}h",
            raw_data
        )
    )

    return sample_rate, channels, samples


def write_wav(
    path: str,
    sample_rate: int,
    channels: int,
    samples: List[int]
):
    """
    Write WAV PCM 16-bit little-endian.
    """

    raw_data = struct.pack(
        f"<{len(samples)}h",
        *samples
    )

    with wave.open(path, "wb") as wav:

        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        wav.writeframes(raw_data)