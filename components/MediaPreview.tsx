'use client';

import type { UploadedFile } from './UploadDropzone';

interface MediaPreviewProps {
  uploadedFile: UploadedFile;
  label?: string;
}

export default function MediaPreview({ uploadedFile, label }: MediaPreviewProps) {
  const { type, url, name } = uploadedFile;

  const Header = () => (
    <div className="px-4 py-3 border-b border-[#1F2A44] flex items-center gap-2">
      <div className="flex gap-1.5">
        <div className="w-2.5 h-2.5 rounded-full bg-[#FF5F57]" />
        <div className="w-2.5 h-2.5 rounded-full bg-[#FFBD2E]" />
        <div className="w-2.5 h-2.5 rounded-full bg-[#28C840]" />
      </div>
      {label && (
        <span className="text-xs font-medium text-blue-400 ml-1">{label}</span>
      )}
      <span className="text-xs text-[#4A5578] ml-1 truncate">{name}</span>
    </div>
  );

  if (type.startsWith('image/')) {
    return (
      <div className="rounded-xl border border-[#1F2A44] bg-[#111A2E] overflow-hidden">
        <Header />
        <div className="p-3">
          <img
            src={url}
            alt={name}
            className="w-full h-auto max-h-64 object-contain rounded-lg"
          />
        </div>
      </div>
    );
  }

  if (type.startsWith('video/')) {
    const isAvi = name.toLowerCase().endsWith('.avi') || type === 'video/x-msvideo';

    return (
      <div className="rounded-xl border border-[#1F2A44] bg-[#111A2E] overflow-hidden">
        <Header />
        <div className="p-3 flex items-center justify-center bg-black min-h-[16rem]">
          {isAvi ? (
            <div className="text-center p-6">
              <p className="text-[#8F9BB3] text-sm mb-2">
                Preview is not available for Uncompressed AVI files.
              </p>
              <p className="text-[#4A5578] text-xs">
                (This format is used by Steganography to protect hidden messages from Lossy compression. Please download the file and open it in a media player like VLC to view it.)
              </p>
            </div>
          ) : (
            <video
              key={url}
              src={url}
              controls
              preload="metadata"
              className="w-full rounded-lg max-h-64"
            />
          )}
        </div>
      </div>
    );
  }

  if (type.startsWith('audio/')) {
    return (
      <div className="rounded-xl border border-[#1F2A44] bg-[#111A2E] p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#FF5F57]" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#FFBD2E]" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#28C840]" />
          </div>
          {label && (
            <span className="text-xs font-medium text-blue-400 ml-1">{label}</span>
          )}
          <span className="text-xs text-[#4A5578] ml-1 truncate">{name}</span>
        </div>
        <audio
          key={url}
          src={url}
          controls
          className="w-full"
          style={{ colorScheme: 'dark' }}
        />
      </div>
    );
  }

  return null;
}
