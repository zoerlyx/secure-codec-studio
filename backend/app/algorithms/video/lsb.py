import cv2
import struct

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


def encode_lsb(input_path: str, output_path: str, message: str):
    """
    Steganography LSB for Video.
    We embed the message into the first few frames of the video.
    We use an uncompressed AVI format to prevent lossy compression from corrupting the LSBs.
    """
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Use FFV1 lossless codec to preserve exact pixel values for LSB while keeping file size small
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    message_bytes = message.encode("utf-8")
    payload = MAGIC + struct.pack(">I", len(message_bytes)) + message_bytes
    payload_bits = _bytes_to_bits(payload)

    bit_index = 0
    total_bits = len(payload_bits)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # If there are still bits to embed in this frame
        if bit_index < total_bits:
            # Flatten the frame to easily modify pixels
            flat_frame = frame.reshape(-1)
            
            # Embed bits into this frame
            for i in range(len(flat_frame)):
                if bit_index < total_bits:
                    # Clear LSB and set it to the payload bit
                    flat_frame[i] = (flat_frame[i] & 0xFE) | int(payload_bits[bit_index])
                    bit_index += 1
                else:
                    break
            
            frame = flat_frame.reshape((height, width, 3))
            
        out.write(frame)

    cap.release()
    out.release()
    
    if bit_index < total_bits:
        raise ValueError("Message is too large for this video")


def decode_lsb(input_path: str) -> str:
    """
    Extracts the hidden message from the video frames.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    bits_list = []
    
    # Read the first frame to look for the MAGIC header and length
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Video is empty")
        
    flat_frame = frame.reshape(-1)
    
    # We don't know the message length yet, so we read a safe amount first (e.g. first 64 bits for header + length)
    if len(flat_frame) < 64:
        raise ValueError("Video resolution is too small")
        
    for i in range(64):
        bits_list.append(str(flat_frame[i] & 1))
        
    bits = "".join(bits_list)
    magic = _bits_to_bytes(bits[:32])
    
    if magic != MAGIC:
        cap.release()
        raise ValueError("No hidden message found")
        
    message_length = struct.unpack(">I", _bits_to_bytes(bits[32:64]))[0]
    total_bits_needed = 64 + (message_length * 8)
    
    bits_list = []
    bit_index = 0
    
    # Re-read from beginning to extract everything
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    while True:
        ret, frame = cap.read()
        if not ret or bit_index >= total_bits_needed:
            break
            
        flat_frame = frame.reshape(-1)
        
        for i in range(len(flat_frame)):
            if bit_index < total_bits_needed:
                bits_list.append(str(flat_frame[i] & 1))
                bit_index += 1
            else:
                break
                
    cap.release()
    
    if bit_index < total_bits_needed:
        raise ValueError("Hidden message is corrupted or incomplete")
        
    all_bits = "".join(bits_list)
    message_bits = all_bits[64:total_bits_needed]
    message_bytes = _bits_to_bytes(message_bits)
    
    return message_bytes.decode("utf-8")
