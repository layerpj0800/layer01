'use client';

interface VideoPlayerProps {
  src: string;
}

export default function VideoPlayer({ src }: VideoPlayerProps) {
  return (
    <video src={src} controls autoPlay loop muted className="w-full" />
  );
}
