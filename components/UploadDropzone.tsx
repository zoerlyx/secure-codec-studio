'use client';

import { useRef, useState, useCallback } from 'react';
import { UploadCloud, FileVideo, FileImage, FileAudio, X, CheckCircle } from 'lucide-react';

export interface UploadedFile {
  file: File;
  name: string;
  size: number;
  type: string;
  url: string;
  progress: number;
  status: 'uploading' | 'complete';
}

interface UploadDropzoneProps {
  uploadedFile: UploadedFile | null;
  onFileUpload: (file: UploadedFile) => void;
  onClear: () => void;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getFileIcon(type: string) {
  if (type.startsWith('image/')) return <FileImage className="w-6 h-6 text-blue-400" />;
  if (type.startsWith('video/')) return <FileVideo className="w-6 h-6 text-blue-400" />;
  if (type.startsWith('audio/')) return <FileAudio className="w-6 h-6 text-blue-400" />;
  return <FileVideo className="w-6 h-6 text-blue-400" />;
}

function getFileTypeLabel(type: string): string {
  if (type.startsWith('image/')) return `Image/${type.split('/')[1].toUpperCase()}`;
  if (type.startsWith('video/')) return `Video/${type.split('/')[1].toUpperCase()}`;
  if (type.startsWith('audio/')) return `Audio/${type.split('/')[1].toUpperCase()}`;
  return type;
}

export default function UploadDropzone({ uploadedFile, onFileUpload, onClear }: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = useCallback((file: File) => {
    const url = URL.createObjectURL(file);
    const uploaded: UploadedFile = {
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      url,
      progress: 0,
      status: 'uploading',
    };
    onFileUpload(uploaded);

    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30 + 10;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        onFileUpload({ ...uploaded, progress: 100, status: 'complete' });
      } else {
        onFileUpload({ ...uploaded, progress: Math.floor(progress), status: 'uploading' });
      }
    }, 120);
  }, [onFileUpload]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  if (uploadedFile) {
    return (
      <div className="rounded-xl border border-[#1F2A44] bg-[#0D1526] p-4 transition-all duration-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#1A2540] border border-[#1F2A44] flex items-center justify-center flex-shrink-0">
            {getFileIcon(uploadedFile.type)}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{uploadedFile.name}</p>
            <p className="text-xs text-[#4A5578] mt-0.5">
              {formatBytes(uploadedFile.size)} &bull; {getFileTypeLabel(uploadedFile.type)}
            </p>
          </div>
          <button
            onClick={onClear}
            className="w-7 h-7 rounded-lg bg-[#1A2540] border border-[#1F2A44] flex items-center justify-center text-[#4A5578] hover:text-white hover:border-[#2D3A5A] transition-all duration-150 flex-shrink-0"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="mt-3">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs text-[#4A5578]">
              {uploadedFile.status === 'uploading' ? `${uploadedFile.progress}% Uploading` : '100% Uploaded'}
            </span>
            <span className={`text-xs font-medium flex items-center gap-1 ${uploadedFile.status === 'complete' ? 'text-green-400' : 'text-[#4A5578]'}`}>
              {uploadedFile.status === 'complete' && <CheckCircle className="w-3 h-3" />}
              {uploadedFile.status === 'complete' ? 'Complete' : 'Uploading...'}
            </span>
          </div>
          <div className="w-full h-1.5 rounded-full bg-[#1A2540]">
            <div
              className="h-1.5 rounded-full bg-blue-500 transition-all duration-200"
              style={{ width: `${uploadedFile.progress}%` }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      className={`rounded-xl border-2 border-dashed cursor-pointer flex flex-col items-center justify-center py-14 px-6 transition-all duration-200 ${
        dragging
          ? 'border-blue-500 bg-blue-500/5'
          : 'border-[#1F2A44] bg-[#0D1526] hover:border-blue-500/50 hover:bg-blue-500/5'
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept="image/png,image/jpeg,image/bmp,image/webp,video/mp4,video/x-msvideo,video/quicktime,video/webm,audio/wav,audio/mpeg,audio/ogg,audio/mp4,audio/aac,audio/flac,.png,.jpg,.jpeg,.bmp,.webp,.mp4,.avi,.mov,.mkv,.webm,.wav,.mp3,.ogg,.m4a,.aac,.mpeg,.flac,.lossless"
        onChange={onInputChange}
      />
      <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-4 transition-all duration-200 ${
        dragging ? 'bg-blue-500/20' : 'bg-[#1A2540]'
      }`}>
        <UploadCloud className={`w-7 h-7 transition-colors duration-200 ${dragging ? 'text-blue-400' : 'text-[#4A5578]'}`} />
      </div>
      <p className="text-sm font-medium text-white mb-1">Drop your file or click to upload</p>
      <p className="text-xs text-[#4A5578]">
        🖼 PNG · JPG · BMP · WebP &nbsp;|&nbsp; 🎬 MP4 · AVI · MOV &nbsp;|&nbsp; 🎵 WAV · MP3 · OGG &nbsp;|&nbsp; 📦 .lossless
      </p>
    </div>
  );
}
