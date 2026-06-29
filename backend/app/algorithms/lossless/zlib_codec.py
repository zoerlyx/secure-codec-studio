import zlib
import os

def compress_lossless(input_path: str, output_path: str):
    """
    Compresses a file losslessly using Zlib.
    Reads the raw binary data of any media type and compresses it.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    with open(input_path, 'rb') as f_in:
        raw_data = f_in.read()
        
    compressed_data = zlib.compress(raw_data, level=9)
    
    with open(output_path, 'wb') as f_out:
        f_out.write(compressed_data)

def decompress_lossless(input_path: str, output_path: str):
    """
    Decompresses a .lossless Zlib compressed file.
    Restores the exact original binary data.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
        
    try:
        raw_data = zlib.decompress(compressed_data)
    except zlib.error as e:
        raise ValueError(f"Failed to decompress file: {e}")
        
    with open(output_path, 'wb') as f_out:
        f_out.write(raw_data)
