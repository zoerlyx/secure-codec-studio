import struct

from app.algorithms.audio.delta import read_wav, write_wav


MAGIC = b"SCMS"


def _bytes_to_bits(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def _bits_to_bytes(bits: str) -> bytes:
    result = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            result.append(int(byte, 2))
    return bytes(result)


def encode_lsb(
    input_path: str,
    output_path: str,
    message: str
):
    sample_rate, channels, samples = read_wav(input_path)

    message_bytes = message.encode("utf-8")
    payload = (
        MAGIC +
        struct.pack(">I", len(message_bytes)) +
        message_bytes
    )

    payload_bits = _bytes_to_bits(payload)

    if len(payload_bits) > len(samples):
        raise ValueError("Message is too large for this audio file")

    for i, bit in enumerate(payload_bits):
        unsigned_sample = samples[i] & 0xFFFF
        unsigned_sample = (unsigned_sample & 0xFFFE) | int(bit)
        if unsigned_sample >= 0x8000:
            samples[i] = unsigned_sample - 0x10000
        else:
            samples[i] = unsigned_sample

    write_wav(output_path, sample_rate, channels, samples)


def decode_lsb(
    input_path: str
) -> str:
    _, _, samples = read_wav(input_path)

    # Extract all LSBs
    bits_list = []
    for sample in samples:
        unsigned_sample = sample & 0xFFFF
        bits_list.append(str(unsigned_sample & 1))
    
    bits = "".join(bits_list)

    # MAGIC HEADER (4 BYTE = 32 bit)
    if len(bits) < 32:
        raise ValueError("No hidden message found")
        
    magic_bits = bits[:32]
    magic = _bits_to_bytes(magic_bits)

    if magic != MAGIC:
        raise ValueError("No hidden message found")

    # MESSAGE LENGTH (4 BYTE = 32 bit)
    if len(bits) < 64:
        raise ValueError("No hidden message found")
        
    length_bits = bits[32:64]
    message_length = struct.unpack(">I", _bits_to_bytes(length_bits))[0]

    # MESSAGE
    start = 64
    end = start + (message_length * 8)
    
    if end > len(bits):
        raise ValueError("Hidden message is corrupted or incomplete")

    message_bits = bits[start:end]
    message_bytes = _bits_to_bytes(message_bits)

    return message_bytes.decode("utf-8")
