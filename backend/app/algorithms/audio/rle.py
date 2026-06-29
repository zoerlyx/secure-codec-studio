import struct


def rle_encode(data: bytes) -> bytes:
    """
    Run Length Encoding untuk stream int16.

    Input:
        Delta bytes (int16 little-endian)

    Output tiap run:
        value : int16 (2 byte)
        count : uint16 (2 byte)

    Total:
        4 byte per run
    """

    if not data:
        return b""

    if len(data) % 2 != 0:
        raise ValueError("Invalid delta data")

    values = list(
        struct.unpack(
            f"<{len(data)//2}h",
            data
        )
    )

    encoded = bytearray()

    current = values[0]
    count = 1

    for value in values[1:]:

        if value == current and count < 65535:
            count += 1

        else:

            encoded.extend(
                struct.pack(
                    "<hH",
                    current,
                    count
                )
            )

            current = value
            count = 1

    encoded.extend(
        struct.pack(
            "<hH",
            current,
            count
        )
    )

    return bytes(encoded)


def rle_decode(data: bytes) -> bytes:
    """
    Decode RLE int16 kembali menjadi
    stream delta int16.
    """

    if not data:
        return b""

    if len(data) % 4 != 0:
        raise ValueError("Invalid RLE data")

    decoded = []

    offset = 0

    while offset < len(data):

        value, count = struct.unpack(
            "<hH",
            data[offset:offset + 4]
        )

        decoded.extend([value] * count)

        offset += 4

    return struct.pack(
        f"<{len(decoded)}h",
        *decoded
    )


def compression_ratio(
    original_size: int,
    processed_size: int
) -> float:

    if original_size == 0:
        return 0.0

    return round(
        ((original_size - processed_size) / original_size) * 100,
        2
    )