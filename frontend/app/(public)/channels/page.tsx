/**
 * ChannelListPage fetches and displays channels.
 */
'use client';

import { useEffect, useState } from 'react';

type Channel = {
  id: number;
  name: string;
  description: string;
};

export default function ChannelListPage() {
  const [channels, set_channels] = useState<Channel[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/channels')
      .then((res) => res.json())
      .then((data: Channel[]) => set_channels(data))
      .catch(() => set_channels([]));
  }, []);

  return (
    <ul>
      {channels.map((ch) => (
        <li key={ch.id}>{ch.name}</li>
      ))}
    </ul>
  );
}
