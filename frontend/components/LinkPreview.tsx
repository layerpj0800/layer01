'use client';

import { useEffect, useState } from 'react';

interface PreviewData {
  title: string;
  description: string;
  image: string;
  url: string;
}

export default function LinkPreview({ url }: { url: string }) {
  const [data, setData] = useState<PreviewData | null>(null);

  useEffect(() => {
    fetch(`/api/v1/link-preview?url=${encodeURIComponent(url)}`)
      .then((res) => res.json())
      .then((d) => setData(d))
      .catch(() => setData(null));
  }, [url]);

  if (!data) return null;

  return (
    <a href={data.url} className="block border p-4">
      {data.image && <img src={data.image} alt={data.title} className="mb-2" />}
      <h3 className="font-bold">{data.title}</h3>
      <p>{data.description}</p>
    </a>
  );
}
