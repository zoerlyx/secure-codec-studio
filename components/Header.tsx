'use client';

import { ShieldCheck } from 'lucide-react';

export default function Header() {
  return (
    <header className="w-full border-b border-[#1F2A44] bg-[#0B1220]/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="w-full px-6 md:px-10 lg:px-16 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <ShieldCheck className="w-7 h-7 text-white" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col leading-tight gap-0.5">
            <span className="text-[18px] font-semibold text-white tracking-tight">Secure Codec Studio</span>
            <span className="text-[12px] text-[#4A5578] font-medium">Multimedia Compression &amp; Steganography Tool</span>
          </div>
        </div>
      </div>
    </header>
  );
}
