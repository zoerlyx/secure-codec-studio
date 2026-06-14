'use client';

import { useState, useCallback } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ModeSelector, { type Mode } from '@/components/ModeSelector';
import UploadDropzone, { type UploadedFile } from '@/components/UploadDropzone';
import ActionPanel from '@/components/ActionPanel';
import ResultCards, { type ProcessingResult } from '@/components/ResultCards';
import MediaPreview from '@/components/MediaPreview';

export default function Home() {
  const [mode, setMode] = useState<Mode>('compression');
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [secretMessage, setSecretMessage] = useState('');
  const [stegoSubMode, setStegoSubMode] = useState<'hide' | 'extract'>('hide');
  const [compressType, setCompressType] = useState<'lossy' | 'lossless'>('lossy');

  const handleFileUpload = useCallback((file: UploadedFile) => {
    setUploadedFile(file);
    setResult(null);
  }, []);

  const handleClear = useCallback(() => {
    if (uploadedFile?.url) URL.revokeObjectURL(uploadedFile.url);
    setUploadedFile(null);
    setResult(null);
    setSecretMessage('');
  }, [uploadedFile]);

  const handleModeChange = (newMode: Mode) => {
    setMode(newMode);
    setResult(null);
    setSecretMessage('');
    setStegoSubMode('hide');
    setCompressType('lossy');
  };

  const handleProcess = async () => {
    if (!uploadedFile || uploadedFile.status !== 'complete') return;
    setIsProcessing(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile.file);

      let backendMode = '';
      if (mode === 'compression') backendMode = 'compress';
      else if (mode === 'decompression') backendMode = 'decompress';
      else if (mode === 'steganography') {
        backendMode = stegoSubMode === 'hide' ? 'stego' : 'extract';
      }

      formData.append('mode', backendMode);

      if (mode === 'compression') {
        formData.append('compress_type', compressType);
      }

      if (mode === 'steganography' && stegoSubMode === 'hide' && secretMessage) {
        formData.append('message', secretMessage);
      }

      let response: Response;

try {
  response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/process`,
    {
      method: "POST",
      body: formData,
    }
  );
} catch {
  alert("Cannot connect to backend server.");
  return;
}

      if (!response.ok) {
        let errMsg = `Server error (${response.status})`;
        try {
          const errData = await response.json();
          if (errData.message) errMsg = errData.message;
        } catch {}
        alert(`Processing failed: ${errMsg}`);
        return;
      }

      const data = await response.json();

      let previewUrl: string | undefined;
      let processedUrl: string | undefined;
      let processedName: string | undefined;
      let processedType: string | undefined;

      if (data.download_url) {
        processedUrl = `${process.env.NEXT_PUBLIC_API_URL}${data.download_url}`;

        previewUrl = `${process.env.NEXT_PUBLIC_API_URL}${data.download_url}${
          data.download_url.endsWith(".lossless") ? "?preview=true" : ""
        }`;
        processedName = data.download_url.split('/').pop()?.split('?')[0];

        const parts = processedName?.split('.') ?? [];
        let ext = parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
        if (ext === 'lossless' && parts.length >= 3) {
           ext = parts[parts.length - 2].toLowerCase();
        }
        
        const extToMime: Record<string, string> = {
          mp4: 'video/mp4', avi: 'video/x-msvideo', mov: 'video/quicktime', mkv: 'video/x-matroska',
          png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', bmp: 'image/bmp', webp: 'image/webp',
          wav: 'audio/wav', mp3: 'audio/mpeg', ogg: 'audio/ogg', m4a: 'audio/mp4', aac: 'audio/aac', flac: 'audio/flac'
        };
        processedType = extToMime[ext] ?? uploadedFile.type;
      }

      setResult({
        originalSize: data.original_size,
        processedSize: data.processed_size,
        ratio: data.compression_ratio,
        processingTime: data.processing_time_ms,
        mode,
        stegoStatus:
          mode === 'steganography' ? data.status : undefined,
        extractedMessage: backendMode === 'extract' ? data.message : undefined,
        processedUrl, // For the download button
        previewUrl,   // For the MediaPreview component
        processedName,
        processedType,
        psnr: data.psnr,
        mse:  data.mse,
      });
    } catch (error) {
      console.error('Error during processing:', error);
      alert('An error occurred while processing the file.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Show original file preview whenever a file is uploaded (both before AND after processing)
  const isMediaFile =
    uploadedFile?.status === 'complete' &&
    (uploadedFile.type.startsWith('image/') ||
     uploadedFile.type.startsWith('video/') ||
     uploadedFile.type.startsWith('audio/') ||
     uploadedFile.name.endsWith('.lossless') ||
     result?.previewUrl);

  return (
    <div className="min-h-screen flex flex-col bg-[#0B1220] text-white">
      <Header />

      <main className="flex-grow w-full max-w-2xl mx-auto px-4 py-10 flex flex-col gap-5">
        {/* Mode Selector */}
        <ModeSelector mode={mode} onChange={handleModeChange} />

        {/* Upload Section */}
        <div className="rounded-2xl border border-[#1F2A44] bg-[#111A2E] p-5 flex flex-col gap-4">
          <UploadDropzone
            uploadedFile={uploadedFile}
            onFileUpload={handleFileUpload}
            onClear={handleClear}
          />

          {/* Action Panel — only shows when file is uploaded */}
          {uploadedFile && uploadedFile.status === 'complete' && (
            <div className="animate-fadeIn">
              <ActionPanel
                mode={mode}
                hasFile={uploadedFile.status === 'complete'}
                isProcessing={isProcessing}
                secretMessage={secretMessage}
                onSecretMessageChange={setSecretMessage}
                stegoSubMode={stegoSubMode}
                onStegoSubModeChange={setStegoSubMode}
                compressType={compressType}
                onCompressTypeChange={setCompressType}
                onProcess={handleProcess}
              />
            </div>
          )}
        </div>

        {/* Processing skeleton */}
        {isProcessing && (
          <div className="rounded-xl border border-[#1F2A44] bg-[#111A2E] p-5 animate-pulse">
            <div className="h-4 w-36 rounded bg-[#1F2A44] mb-4" />
            <div className="grid grid-cols-4 gap-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="rounded-xl border border-[#1F2A44] bg-[#0D1526] px-4 py-3">
                  <div className="h-3 w-12 rounded bg-[#1F2A44] mb-3" />
                  <div className="h-5 w-16 rounded bg-[#1F2A44]" />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Result Cards */}
        {result && !isProcessing && <ResultCards result={result} />}

        {/* ── PREVIEW SECTION ──────────────────────────────────────────────── */}
        {!isProcessing && isMediaFile && (
          <>
            {/* Original file preview — always shown when a file is loaded */}
            <MediaPreview
              label="Original File"
              uploadedFile={uploadedFile!}
            />

            {/* Processed file preview — shown after successful processing */}
            {result?.previewUrl && (
              <MediaPreview
                label={
                  mode === 'compression'   ? 'Compressed File' :
                  mode === 'decompression' ? 'Decompressed File' :
                  'Stego File'
                }
                uploadedFile={{
                  file:     new File([], result.processedName ?? 'processed'),
                  name:     result.processedName ?? 'processed',
                  size:     result.processedSize,
                  type:     result.processedType ?? uploadedFile!.type,
                  url:      result.previewUrl,
                  progress: 100,
                  status:   'complete',
                }}
              />
            )}
          </>
        )}

        {/* Empty state hint */}
        {!uploadedFile && (
          <p className="text-center text-xs text-[#2D3A5A] mt-2">
            Upload a file above to get started
          </p>
        )}
      </main>
      <Footer />
    </div>
  );
}
