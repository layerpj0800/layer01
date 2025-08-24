'use client';

import { useState } from 'react';

export default function NewPostPage() {
  const [channelId, setChannelId] = useState('');
  const [content, setContent] = useState('');
  const [type, setType] = useState('general');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await fetch('/api/v1/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ channel_id: Number(channelId), content, type }),
    });
    setChannelId('');
    setContent('');
    setType('general');
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <input
        type="number"
        placeholder="Channel ID"
        value={channelId}
        onChange={(e) => setChannelId(e.target.value)}
        className="border p-2"
        required
      />
      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="border p-2"
        required
      />
      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
        className="border p-2"
      >
        <option value="general">General</option>
        <option value="stock-briefing">Stock Briefing</option>
      </select>
      <button type="submit" className="bg-blue-500 text-white p-2">
        Create Post
      </button>
    </form>
  );
}
