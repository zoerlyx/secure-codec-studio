'use client';

import { Loader2, Archive, FolderOpen, EyeOff, Eye, HelpCircle } from 'lucide-react';
import type { Mode } from './ModeSelector';

interface ActionPanelProps {
  mode: Mode;
  hasFile: boolean;
  isProcessing: boolean;
  secretMessage: string;
  onSecretMessageChange: (val: string) => void;
  stegoSubMode: 'hide' | 'extract';
  onStegoSubModeChange: (val: 'hide' | 'extract') => void;
  compressType: 'lossy' | 'lossless';
  onCompressTypeChange: (val: 'lossy' | 'lossless') => void;
  onProcess: () => void;
}

export default function ActionPanel({
  mode,
  hasFile,
  isProcessing,
  secretMessage,
  onSecretMessageChange,
  stegoSubMode,
  onStegoSubModeChange,
  compressType,
  onCompressTypeChange,
  onProcess,
}: ActionPanelProps) {
  const disabled = !hasFile || isProcessing;

  if (mode === 'compression') {
    return (
      <div className="flex flex-col gap-4">
        <div className="flex items-center p-1 rounded-xl bg-[#0B1220] border border-[#1F2A44] gap-1 group/tooltip">
          <button
            onClick={() => onCompressTypeChange('lossy')}
            className={`flex-1 flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 ${
              compressType === 'lossy'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-[#6B7FA8] hover:text-white hover:bg-[#1F2A44]'
            }`}
          >
            Lossy
          </button>
          <button
            onClick={() => onCompressTypeChange('lossless')}
            className={`flex-1 flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 ${
              compressType === 'lossless'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-[#6B7FA8] hover:text-white hover:bg-[#1F2A44]'
            }`}
          >
            Lossless
          </button>

          <div className="flex items-center px-2">
            <div className="relative group/icon cursor-help">
              <HelpCircle className="w-4 h-4 text-[#4A5578] hover:text-blue-400 transition-colors" />
              
              <div className="absolute right-0 bottom-full mb-2 w-64 p-3 bg-[#111A2E] border border-[#1F2A44] rounded-lg shadow-xl opacity-0 invisible group-hover/icon:opacity-100 group-hover/icon:visible transition-all duration-200 z-50">
                <div className="text-xs text-white space-y-2">
                  <p>
                    <span className="font-bold text-red-400">Lossy:</span> Ukuran file menjadi jauh lebih kecil, namun kualitas berkurang secara permanen (menjadi format biasa). Saat di-Decompress, data asli tidak kembali.
                  </p>
                  <p>
                    <span className="font-bold text-green-400">Lossless:</span> Menggunakan algoritma Zlib. Ukuran sedikit menyusut (menjadi format .lossless). Saat di-Decompress, file akan kembali 100% sempurna seperti semula.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          onClick={onProcess}
          disabled={disabled}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-150"
        >
          {isProcessing ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Archive className="w-4 h-4" />
          )}
          {isProcessing ? 'Compressing...' : 'Compress File'}
        </button>
      </div>
    );
  }

  if (mode === 'decompression') {
    return (
      <button
        onClick={onProcess}
        disabled={disabled}
        className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-150"
      >
        {isProcessing ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <FolderOpen className="w-4 h-4" />
        )}
        {isProcessing ? 'Restoring...' : 'Restore File'}
      </button>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex gap-1 p-1 rounded-xl bg-[#0B1220] border border-[#1F2A44]">
        <button
          onClick={() => onStegoSubModeChange('hide')}
          className={`flex-1 flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 ${
            stegoSubMode === 'hide'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
              : 'text-[#6B7FA8] hover:text-white hover:bg-[#1F2A44]'
          }`}
        >
          <EyeOff className="w-3.5 h-3.5" />
          Hide Message
        </button>
        <button
          onClick={() => onStegoSubModeChange('extract')}
          className={`flex-1 flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 ${
            stegoSubMode === 'extract'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
              : 'text-[#6B7FA8] hover:text-white hover:bg-[#1F2A44]'
          }`}
        >
          <Eye className="w-3.5 h-3.5" />
          Extract Message
        </button>
      </div>

      {stegoSubMode === 'hide' && (
        <textarea
          value={secretMessage}
          onChange={(e) => onSecretMessageChange(e.target.value)}
          placeholder="Enter your secret message..."
          rows={3}
          className="w-full rounded-xl border border-[#1F2A44] bg-[#0D1526] text-white text-sm placeholder-[#3A4A6A] px-4 py-3 resize-none outline-none focus:border-blue-500/60 focus:ring-1 focus:ring-blue-500/20 transition-all duration-150"
        />
      )}

      <button
        onClick={onProcess}
        disabled={disabled || (stegoSubMode === 'hide' && !secretMessage.trim())}
        className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-150"
      >
        {isProcessing ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : stegoSubMode === 'hide' ? (
          <EyeOff className="w-4 h-4" />
        ) : (
          <Eye className="w-4 h-4" />
        )}
        {isProcessing
          ? 'Processing...'
          : stegoSubMode === 'hide'
          ? 'Hide Message'
          : 'Extract Message'}
      </button>
    </div>
  );
}
