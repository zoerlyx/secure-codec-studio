from itertools import groupby


def rle_encode(data: bytes) -> bytes:
    """
    Encode bytes menggunakan Run Length Encoding sederhana.
    Format:
    [count][value]
    """

    encoded = bytearray()

    for value, group in groupby(data):
        count = len(list(group))

        while count > 255:
            encoded.append(255)
            encoded.append(value)
            count -= 255

        encoded.append(count)
        encoded.append(value)

    return bytes(encoded)


def rle_decode(data: bytes) -> bytes:
    """
    Decode bytes hasil Run Length Encoding.
    """

    if len(data) % 2 != 0:
        raise ValueError("Invalid RLE data")

    decoded = bytearray()

    for i in range(0, len(data), 2):
        count = data[i]
        value = data[i + 1]

        decoded.extend([value] * count)

    return bytes(decoded)


def compression_ratio(original_size: int, processed_size: int) -> float:
    """
    Menghitung compression ratio.
    Nilai > 1 berarti file berhasil diperkecil.
    Nilai < 1 berarti file menjadi lebih besar.
    """

    if processed_size == 0:
        return 0.0

    return round(original_size / processed_size, 2)