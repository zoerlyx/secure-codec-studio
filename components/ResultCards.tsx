'use client';

import { FileIcon, FileArchive, BarChart2, Clock, Download, CheckCircle, XCircle, MessageSquare, Activity, Gauge } from 'lucide-react';
import type { Mode } from './ModeSelector';

export interface ProcessingResult {
  originalSize: number;
  processedSize: number;
  ratio: number;
  processingTime: number;
  mode: Mode;
  stegoStatus?: 'success' | 'failed';
  extractedMessage?: string;
  processedUrl?: string;
  previewUrl?: string;
  processedName?: string;
  processedType?: string;
  psnr?: number | null;
  mse?: number | null;
}

interface ResultCardsProps {
  result: ProcessingResult;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub?: string;
}

function StatCard({ icon, label, value, sub }: StatCardProps) {
  return (
    <div className="flex flex-col gap-2 rounded-xl border border-[#1F2A44] bg-[#0D1526] px-4 py-3">
      <div className="flex items-center gap-2 text-[#4A5578]">
        {icon}
        <span className="text-xs font-medium">{label}</span>
      </div>
      <p className="text-lg font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-[#4A5578]">{sub}</p>}
    </div>
  );
}

export default function ResultCards({ result }: ResultCardsProps) {
  const isSteganography = result.mode === 'steganography';

  const handleDownload = () => {
    if (!result.processedUrl || !result.processedName) return;
    // Use native browser download to avoid hanging the page on large files (like uncompressed AVI)
    const link = document.createElement('a');
    link.href = `${result.processedUrl}?download=true`;
    link.download = result.processedName;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="rounded-xl border border-[#1F2A44] bg-[#111A2E] p-5 animate-fadeIn">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-white">Processing Results</h3>
        <span className="text-xs text-[#4A5578] font-mono">ID: #SC-{Math.floor(Math.random() * 90000 + 10000)}</span>
      </div>

      <div className={`grid gap-3 ${isSteganography ? 'grid-cols-2' : 'grid-cols-2 sm:grid-cols-4'}`}>
        <StatCard
          icon={<FileIcon className="w-3.5 h-3.5" />}
          label="Original"
          value={formatBytes(result.originalSize)}
        />
        {!isSteganography && (
          <StatCard
            icon={<FileArchive className="w-3.5 h-3.5" />}
            label={result.mode === 'compression' ? 'Compressed' : 'Restored'}
            value={formatBytes(result.processedSize)}
          />
        )}
        {!isSteganography && (
          <StatCard
            icon={<BarChart2 className="w-3.5 h-3.5" />}
            label="Ratio"
            value={`${result.ratio}%`}
          />
        )}
        <StatCard
          icon={<Clock className="w-3.5 h-3.5" />}
          label="Time"
          value={`${result.processingTime}ms`}
        />
        {isSteganography && (
          <div className="flex flex-col gap-2 rounded-xl border border-[#1F2A44] bg-[#0D1526] px-4 py-3">
            <div className="flex items-center gap-2 text-[#4A5578]">
              {result.stegoStatus === 'success' ? (
                <CheckCircle className="w-3.5 h-3.5 text-green-400" />
              ) : (
                <XCircle className="w-3.5 h-3.5 text-red-400" />
              )}
              <span className="text-xs font-medium">Status</span>
            </div>
            <p className={`text-lg font-bold ${result.stegoStatus === 'success' ? 'text-green-400' : 'text-red-400'}`}>
              {result.stegoStatus === 'success' ? 'Success' : 'Failed'}
            </p>
          </div>
        )}
      </div>

      {isSteganography && result.extractedMessage && (
        <div className="mt-3 rounded-xl border border-[#1F2A44] bg-[#0D1526] px-4 py-3">
          <div className="flex items-center gap-2 text-[#4A5578] mb-2">
            <MessageSquare className="w-3.5 h-3.5" />
            <span className="text-xs font-medium">Extracted Message</span>
          </div>
          <p className="text-sm text-white font-mono break-all">{result.extractedMessage}</p>
        </div>
      )}

      {result.processedUrl && (
        <button
          onClick={handleDownload}
          className="mt-4 w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 hover:bg-blue-500 transition-all duration-150"
        >
          <Download className="w-4 h-4" />
          Download Processed File
        </button>
      )}

      {!isSteganography && (result.psnr != null || result.mse != null) && (
        <div className="mt-3 grid grid-cols-2 gap-3">
          {result.psnr != null && (
            <StatCard
              icon={<Activity className="w-3.5 h-3.5" />}
              label="PSNR"
              value={result.psnr === Infinity ? '∞ dB' : `${result.psnr} dB`}
              sub="Peak Signal-to-Noise Ratio"
            />
          )}
          {result.mse != null && (
            <StatCard
              icon={<Gauge className="w-3.5 h-3.5" />}
              label="MSE"
              value={`${result.mse}`}
              sub="Mean Squared Error"
            />
          )}
        </div>
      )}
    </div>
  );
}
