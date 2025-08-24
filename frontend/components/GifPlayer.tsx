'use client';

interface GifPlayerProps {
  src: string;
  alt?: string;
}

export default function GifPlayer({ src, alt }: GifPlayerProps) {
  return <img src={src} alt={alt ?? 'gif'} className="w-full" />;
}
