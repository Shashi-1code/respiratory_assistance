import React from "react";

export default function MessageBubble({ sender, text }) {
  const isUser = sender === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] p-3 rounded-2xl shadow-md text-sm whitespace-pre-line ${isUser ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-100"}`}
      >
        {text}
      </div>
    </div>
  );
}
