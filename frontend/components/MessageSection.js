// frontend/components/MessageSection.js
"use client";

import { useState } from "react";

export default function MessageSection({ setBackendResponse }) {
  const [userMessage, setUserMessage] = useState("");

  const handleSendMessage = async () => {
    if (!userMessage) {
      alert("Please enter a message.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });
      if (response.ok) {
        const data = await response.json();
        setBackendResponse(data.message || "No response received.");
      } else {
        const data = await response.json();
        alert(data.error || "Error processing message.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while sending the message.");
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-2">Send a Message</h2>
      <input
        type="text"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
        className="border p-2 w-full mb-2"
        placeholder="Enter your message"
      />
      <button
        onClick={handleSendMessage}
        className="px-4 py-2 bg-purple-500 text-white rounded"
      >
        Send Message
      </button>
    </div>
  );
}
