'use client';

import { useRef } from 'react';

interface PdfViewerProps {
  src: string;
  pages: number;
}

export function PdfViewer({ src, pages }: PdfViewerProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  const goToPage = (p: number) => {
    if (iframeRef.current) {
      iframeRef.current.src = `${src}#page=${p}&toolbar=0`;
    }
  };

  return (
    <div className="flex">
      <nav className="mr-4">
        <ul>
          {Array.from({ length: pages }, (_, i) => (
            <li key={i}>
              <button onClick={() => goToPage(i + 1)} className="underline">
                Page {i + 1}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <iframe
        ref={iframeRef}
        src={`${src}#toolbar=0`}
        className="flex-1 h-screen"
        title="PDF document"
      />
    </div>
  );
}
