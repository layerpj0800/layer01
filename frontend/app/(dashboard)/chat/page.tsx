"use client";

import { useEffect, useState } from "react";

interface Message {
  id: number;
  content: string;
  pinned: boolean;
  attachment?: string | null;
  reactions?: Record<string, number>;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    fetch("/api/v1/messages").then(res => res.json()).then(setMessages);
    const es = new EventSource("/api/v1/messages/stream");
    es.onmessage = (event) => {
      const data: Message = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };
    return () => es.close();
  }, []);

  const sendMessage = async () => {
    await fetch("/api/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: input }),
    });
    setInput("");
  };

  const addReaction = (id: number, emoji: string) => {
    setMessages(msgs =>
      msgs.map(m =>
        m.id === id
          ? {
              ...m,
              reactions: { ...m.reactions, [emoji]: (m.reactions?.[emoji] || 0) + 1 },
            }
          : m
      )
    );
  };

  return (
    <div className="p-4">
      <div className="space-y-2">
        {messages.map(m => (
          <div key={m.id} className="border p-2">
            <p>{m.content}</p>
            <div className="space-x-2 mt-1">
              {['👍', '❤️', '😂'].map(e => (
                <button key={e} onClick={() => addReaction(m.id, e)}>
                  {e} {m.reactions?.[e] || 0}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 flex space-x-2">
        <input
          className="border flex-1 p-1"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a message"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
