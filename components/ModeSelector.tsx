'use client';

export type Mode = 'compression' | 'decompression' | 'steganography';

interface ModeSelectorProps {
  mode: Mode;
  onChange: (mode: Mode) => void;
}

const modes: { key: Mode; label: string }[] = [
  { key: 'compression', label: 'Compression' },
  { key: 'decompression', label: 'Decompression' },
  { key: 'steganography', label: 'Steganography' },
];

export default function ModeSelector({ mode, onChange }: ModeSelectorProps) {
  return (
    <div className="flex gap-1 p-1 rounded-xl bg-[#0B1220] border border-[#1F2A44]">
      {modes.map(({ key, label }) => (
        <button
          key={key}
          onClick={() => onChange(key)}
          className={`flex-1 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 ${
            mode === key
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
              : 'text-[#6B7FA8] hover:text-white hover:bg-[#1F2A44]'
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
