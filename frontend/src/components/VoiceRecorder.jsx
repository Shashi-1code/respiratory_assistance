import React, { useState, useRef } from "react";

export default function VoiceRecorder({ onResponse }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleStart = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorderRef.current = mediaRecorder;
    audioChunksRef.current = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", blob, "recording.webm");

      try {
        const res = await fetch("http://localhost:5000/api/analyze", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        onResponse(data.transcript, data.response);
      } catch (err) {
        onResponse("", "Failed to fetch response from server.");
      }
    };

    mediaRecorder.start();
    setRecording(true);
  };

  const handleStop = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div className="mt-4 flex gap-2">
      {!recording ? (
        <button
          className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-full shadow"
          onClick={handleStart}
        >
          🎙️ Start
        </button>
      ) : (
        <button
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-full shadow"
          onClick={handleStop}
        >
          ⏹️ Stop
        </button>
      )}
    </div>
  );
}
