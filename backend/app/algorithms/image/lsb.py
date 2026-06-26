import struct

from PIL import Image


MAGIC = b"SCMS"


def _bytes_to_bits(data: bytes) -> str:
    """
    Mengubah bytes menjadi string bit.
    """

    return "".join(format(byte, "08b") for byte in data)


def _bits_to_bytes(bits: str) -> bytes:
    """
    Mengubah string bit menjadi bytes.
    """

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
    """
    Menyisipkan pesan ke dalam image menggunakan LSB.
    """

    image = Image.open(input_path).convert("RGB")

    pixels = bytearray(image.tobytes())

    message_bytes = message.encode("utf-8")

    payload = (
        MAGIC +
        struct.pack(">I", len(message_bytes)) +
        message_bytes
    )

    payload_bits = _bytes_to_bits(payload)

    if len(payload_bits) > len(pixels):
        raise ValueError("Message is too large for this image")

    for i, bit in enumerate(payload_bits):

        pixels[i] = (
            pixels[i] & 0b11111110
        ) | int(bit)

    stego = Image.frombytes(
        "RGB",
        image.size,
        bytes(pixels)
    )

    stego.save(
        output_path,
        format="PNG"
    )


def decode_lsb(
    input_path: str
) -> str:
    """
    Mengekstrak pesan dari image.
    """

    image = Image.open(input_path).convert("RGB")

    pixels = image.tobytes()

    bits = "".join(
        str(pixel & 1)
        for pixel in pixels
    )

    # ==========================
    # MAGIC HEADER (4 BYTE)
    # ==========================

    magic_bits = bits[:32]

    magic = _bits_to_bytes(
        magic_bits
    )

    if magic != MAGIC:
        raise ValueError(
            "No hidden message found"
        )

    # ==========================
    # MESSAGE LENGTH (4 BYTE)
    # ==========================

    length_bits = bits[32:64]

    message_length = struct.unpack(
        ">I",
        _bits_to_bytes(length_bits)
    )[0]

    # ==========================
    # MESSAGE
    # ==========================

    start = 64
    end = start + (message_length * 8)

    message_bits = bits[start:end]

    message_bytes = _bits_to_bytes(
        message_bits
    )

    return message_bytes.decode("utf-8")