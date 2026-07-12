import cv2
import numpy as np


def calculate_psnr(original_path: str, processed_path: str) -> float:
    """
    Calculate the Peak Signal-to-Noise Ratio (PSNR) between two images.
    Returns infinity if the images are identical.
    """
    img1 = cv2.imread(original_path)
    img2 = cv2.imread(processed_path)
    
    if img1 is None or img2 is None:
        return 0.0

    # Ensure same size for comparison
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    mse = np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
        
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return round(float(psnr), 2)


def calculate_mse(original_path: str, processed_path: str) -> float:
    """
    Calculate the Mean Squared Error (MSE) between two images.
    Returns 0 if the images are identical.
    """
    img1 = cv2.imread(original_path)
    img2 = cv2.imread(processed_path)
    
    if img1 is None or img2 is None:
        return 0.0

    # Ensure same size for comparison
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    mse = np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)
    
    return round(float(mse), 2)


import wave
import struct

def get_audio_samples(path: str):
    with wave.open(path, 'rb') as wav:
        n_channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        n_frames = wav.getnframes()
        frames = wav.readframes(n_frames)
        
        if sampwidth == 1:
            fmt = f"{n_frames * n_channels}B"
        elif sampwidth == 2:
            fmt = f"<{n_frames * n_channels}h"
        else:
            return None
            
        return np.array(struct.unpack(fmt, frames), dtype=np.float64)

def calculate_audio_mse(original_path: str, processed_path: str) -> float:
    samples1 = get_audio_samples(original_path)
    samples2 = get_audio_samples(processed_path)
    
    if samples1 is None or samples2 is None:
        return 0.0
        
    # If sizes differ (e.g., due to downsampling/upsampling logic), match to smaller
    min_len = min(len(samples1), len(samples2))
    s1 = samples1[:min_len]
    s2 = samples2[:min_len]
    
    mse = np.mean((s1 - s2) ** 2)
    return round(float(mse), 2)

def calculate_audio_psnr(original_path: str, processed_path: str) -> float:
    mse = calculate_audio_mse(original_path, processed_path)
    if mse == 0:
        return float('inf')
        
    # Max value for 16-bit audio
    max_val = 32767.0
    psnr = 20 * np.log10(max_val / np.sqrt(mse))
    
    return round(float(psnr), 2)


def calculate_video_mse(original_path: str, processed_path: str) -> float:
    cap1 = cv2.VideoCapture(original_path)
    cap2 = cv2.VideoCapture(processed_path)
    
    if not cap1.isOpened() or not cap2.isOpened():
        return 0.0
        
    mses = []
    
    for _ in range(10):
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not ret1 or not ret2:
            break
            
        if frame1.shape != frame2.shape:
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
            
        mse = np.mean((frame1.astype(np.float64) - frame2.astype(np.float64)) ** 2)
        mses.append(mse)
        
    cap1.release()
    cap2.release()
    
    if not mses:
        return 0.0
        
    return round(float(np.mean(mses)), 2)


def calculate_video_psnr(original_path: str, processed_path: str) -> float:
    mse = calculate_video_mse(original_path, processed_path)
    if mse == 0:
        return float('inf')
        
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return round(float(psnr), 2)
