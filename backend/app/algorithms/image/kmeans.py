import cv2
import numpy as np


def compress_image_kmeans(input_path: str, output_path: str, k: int = 128):
    """
    Compress an image using K-Means Color Quantization.
    K=128 gives near-original quality with meaningful compression.
    Higher K = better quality, lower K = smaller file but more color loss.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Cannot read image")

    # Reshape the image to a 2D array of pixels and 3 color values (RGB)
    Z = img.reshape((-1, 3))
    
    # Convert to np.float32
    Z = np.float32(Z)
    
    # Define criteria, number of clusters(K) and apply kmeans()
    # Reduced iterations to 10 and attempts to 1 for massive speedup
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    ret, label, center = cv2.kmeans(Z, k, None, criteria, 1, cv2.KMEANS_PP_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    
    # Save the compressed image
    if output_path.lower().endswith(('.jpg', '.jpeg')):
        cv2.imwrite(output_path, res2, [cv2.IMWRITE_JPEG_QUALITY, 50])
    else:
        cv2.imwrite(output_path, res2)


def decompress_image_kmeans(input_path: str, output_path: str):
    """
    Since color quantization is lossy, decompression is technically just reading
    the saved quantized image. You cannot perfectly recover the original colors.
    For MVP purposes, we just copy or read/write the image.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Cannot read image")
    
    cv2.imwrite(output_path, img)
