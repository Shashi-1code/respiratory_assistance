import React, { useState } from "react";
import MessageBubble from "./MessageBubble";
import VoiceRecorder from "./VoiceRecorder";

export default function ChatApp() {
  const [messages, setMessages] = useState([]);

  const handleNewMessage = (transcript, response) => {
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: transcript },
      { sender: "bot", text: response },
    ]);
  };

  return (
    <div className="flex flex-col items-center p-4 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">🩺 Respiratory Assistant</h1>
      <div className="bg-gray-800 w-full rounded-2xl p-4 space-y-2 overflow-y-auto h-[70vh]">
        {messages.map((msg, index) => (
          <MessageBubble key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <VoiceRecorder onResponse={handleNewMessage} />
    </div>
  );
}