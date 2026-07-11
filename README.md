# Secure Multimedia Codec Studio
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000)
![Railway](https://img.shields.io/badge/Backend-Railway-0B0D0E)
![License](https://img.shields.io/badge/License-MIT-yellow)

A full-stack web application for demonstrating **lossless multimedia compression** and **steganography** algorithms on digital media. This project is developed using a Single Page Application (SPA) architecture with **Next.js** as the frontend and **FastAPI** as the backend.

---
### 🌐 Live Demo

- Frontend:
https://secure-codec-studio.vercel.app/

- Backend API:
https://secure-codec-studio-production.up.railway.app

---

## Overview

Secure Multimedia Codec Studio is a full-stack web application that demonstrates multimedia compression and Least Significant Bit (LSB) steganography across images, audio, and video.

The application supports both **Lossless Compression** and **Lossy Compression**, allowing users to understand the fundamental differences between reversible and irreversible compression methods through an interactive web interface and provides performance metrics such as compression ratio, processing time, PSNR, and MSE where applicable.

---
## Highlights

- 🌐 Live Production Deployment
- 🖼️ Image, Audio & Video Compression
- 🔒 Least Significant Bit (LSB) Steganography
- 📊 Compression Analytics (Ratio, PSNR, MSE)
- ⚡ Built with Next.js + FastAPI
- ☁️ Deployed on Vercel & Railway

---

## 📸 Application Gallery

| 1️⃣ Main User Interface | 2️⃣ Integrated Media Player |
| :---: | :---: |
| <img width="100%" alt="Main User Interface" src="https://github.com/user-attachments/assets/0c16ab7b-2c43-484c-9414-8ee4d5774596" /> | <img width="100%" alt="Integrated Media Player" src="https://github.com/user-attachments/assets/9fea3b45-9135-472b-b8b9-7f648c84644a" /> |
| **Clean & Responsive UI**: The main dashboard featuring a dark-themed dropzone and mode selection. | **Media Preview**: Built-in player to instantly render and playback processed Video, Audio, and Images. |

| 3️⃣ Lossless Compression Analytics | 4️⃣ Lossy Compression Analytics |
| :---: | :---: |
| <img width="100%" alt="Lossless Analytics" src="https://github.com/user-attachments/assets/8757ecb3-913f-49b9-978e-819a21fbdfbe" /> | <img width="100%" alt="Lossy Analytics" src="https://github.com/user-attachments/assets/2ebc7262-73ed-4583-9914-b71a40674185" /> |
| **Data Preservation**: Results showing exact original data retention using the Zlib algorithm. | **Size Optimization**: Results demonstrating massive file size reduction and PSNR/MSE quality metrics. |

| 5️⃣ Steganography (Hide Message) | 6️⃣ Steganography (Extract Message) |
| :---: | :---: |
| <img width="100%" alt="Steganography Hide" src="https://github.com/user-attachments/assets/ef908d97-96ef-43c7-8766-cf3830cf338e" /> | <img width="100%" alt="Steganography Extract" src="https://github.com/user-attachments/assets/0103b111-ab0d-42b3-8c0c-5c72472ceb9f" /> |
| **Secure Embedding**: Hiding a secret text message inside a media file via LSB. | **Data Extraction**: Successfully extracting and reading the hidden secret text from a stego file. |

---
# Technology Stack
## Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- Lucide Icons
---
## Backend
- FastAPI
- Python
- OpenCV
- FFmpeg (FFV1, H.264)
- Zlib

---
# Features

Secure Multimedia Codec Studio supports multimedia compression and steganography across images, audio, and video through a unified processing workflow.

## Compression Modes

| Mode | Description | Decompression |
|------|-------------|---------------|
| **Lossless Compression** | Reversible compression that preserves the original data using the Zlib algorithm. | ✅ Supported |
| **Lossy Compression** | Irreversible compression that reduces file size by sacrificing part of the original information. | ❌ Not Supported |
| **Steganography** | Hides and extracts secret text messages using the Least Significant Bit (LSB) technique. | N/A |

## Compression Comparison

| Feature | Lossless | Lossy |
|----------|:--------:|:------:|
| Original Data Preserved | ✅ | ❌ |
| Can Be Decompressed | ✅ | ❌ |
| Compression Ratio | Moderate | High |
| Image Quality | Unchanged | Reduced |
| Best Use Case | Archiving & Editing | Distribution & Storage |

---

## Supported Media

| Media | Compression Algorithms | Steganography | Supported Formats | Max File Size |
|--------|------------------------|---------------|-------------------|---------------|
| **Image** | Zlib (Lossless), OpenCV JPEG (Lossy) | LSB | PNG, JPG, JPEG, BMP, WebP | 5 MB |
| **Audio** | Zlib (Lossless), FFmpeg libmp3lame (Lossy) | LSB | WAV, MP3, OGG, M4A, AAC, FLAC | 10 MB |
| **Video** | Zlib (Lossless), FFmpeg H.264/libx264 (Lossy) | LSB (FFV1) | MP4, AVI, MOV, MKV | 20 MB |

---

## Processing Capabilities

- **Lossless Compression** with complete data preservation.
- **Lossy Compression** for efficient multimedia storage.
- **Lossless Decompression** for restoring compressed media.
- **LSB Steganography** to embed secret messages.
- **Hidden Message Extraction** from supported steganographic media.
- **Compression Analytics** including Compression Ratio, Processing Time, PSNR, and MSE (where applicable).
- **Integrated Media Preview** for processed images, audio, and video.

---
## Storage

All processed files are temporarily stored inside:

```
backend/tmp/
```

Temporary files are only used during processing.

---

# Project Architecture

```

Secure-Codec-Studio
│
├── app/
│
├── components/
│   ├── ActionPanel.tsx
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── UploadDropzone.tsx
│   ├── ModeSelector.tsx
│   ├── ResultCards.tsx
│   └── MediaPreview.tsx
│
├── hooks/
│
├── lib/
│   ├── api.ts
│   └── utils.ts
│
├── backend/
│   ├── app/
│   │
│   ├── algorithms/
│   │   ├── image/
│   │   ├── audio/
│   │   └── video/
│   │
│   ├── services/
│   │
│   ├── routes.py
│   ├── schemas.py
│   ├── utils.py
│   │
│   └── tmp/
│
└── README.md

```

---

# Backend Architecture

The backend follows a simple layered architecture.

```

Client
│
▼

routes.py

│

▼

validator.py

│

▼

service

│

▼

algorithm

│

▼

response

```

Business logic is placed inside **services**, while algorithms are isolated inside the **algorithms** directory.

---

## Compression Workflow

```text

                    Upload Image
                         │
                         ▼
          Select Compression Method
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      Lossless Compression     Lossy Compression
             │                       │
             ▼                       ▼
        Zlib Algorithm         Quality Reduction
             │                       │
             ▼                       ▼
    Codec File (.lossless)    Optimized Image
             │
             ▼
        Decompression
             │
             ▼
       Original Image Restored

```
# Audio Processing Flow

```text
                     Upload Audio
                          │
                          ▼
           Select Compression Method
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       Lossless Compression     Lossy Compression
              │                       │
              ▼                       ▼
        Zlib Algorithm         FFmpeg libmp3lame
              │                       │
              ▼                       ▼
     Codec File (.lossless)    Optimized Audio
              │
              ▼
         Decompression
              │
              ▼
        Original Audio Restored
```

---

# API Endpoint

## Process File

```
POST /process
```

### Request

Multipart Form Data

| Field | Type | Description |
|--------|------|-------------|
| file | File | Uploaded media |
| mode | String | compress / decompress / stego / extract |
| message | String | Secret message (optional) |

---

### Response

```json
{
    "status": "success",
    "media_type": "image",
    "original_size": 102400,
    "processed_size": 50231,
    "compression_ratio": 50.95,
    "processing_time_ms": 135,
    "message": "Image compressed successfully"
}
```

---
# Quick Start

Before running this project, ensure you have the following installed on your system:
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **FFmpeg**: Must be installed and added to your system's `PATH`. This is **critically required** for Audio and Video processing to work.

## 1. Clone the Repository

```bash
git clone https://github.com/zoerlyx/secure-codec-studio.git
cd secure-codec-studio
```

---

## 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
python run.py
```

Backend will be available at:

```
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

Return to the project root:

```bash
cd ..
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Frontend will be available at:

```
http://localhost:3000
```

---
# API Documentation

The backend provides an interactive Swagger UI for exploring and testing all available API endpoints.

### Production

```
https://secure-codec-studio-production.up.railway.app/docs
```

### Local Development

```
http://127.0.0.1:8000/docs
```

The API documentation includes:

- File processing endpoint
- Request parameters
- Response schema
- Interactive request testing
- Validation errors

---
# Deployment

The application is deployed as a decoupled full-stack architecture.

| Service | Platform | URL |
|----------|----------|-----|
| Frontend | Vercel | https://secure-codec-studio.vercel.app/ |
| Backend API | Railway | https://secure-codec-studio-production.up.railway.app |
| API Docs | Railway Swagger | https://secure-codec-studio-production.up.railway.app/docs |

The frontend communicates with the backend through the `NEXT_PUBLIC_API_URL` environment variable.

---
# Future Improvements

- Stereo WAV support
- Advanced lossy image compression
- Better compression ratio for audio
- Progressive processing
- Batch processing
- Download manager

---

# License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# Author
**Fardho Zurrahman**

**Muhammad Ridwan Ihsan**

**Muhammad Wiguna Ilham**

---
Data Science Enthusiast

Built with using Next.js and FastAPI.
