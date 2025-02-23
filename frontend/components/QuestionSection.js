// frontend/components/QuestionSection.js
"use client";

import { useState } from "react";

export default function QuestionSection({ setAnswer }) {
  const [question, setQuestion] = useState("");

  const handleAsk = async () => {
    if (!question) {
      alert("Please enter a question.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer || "No answer received.");
      } else {
        const data = await response.json();
        alert(data.error || "Error getting answer.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while asking the question.");
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Ask a Question</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="border p-2 w-full mb-2"
        placeholder="Enter your question"
      />
      <button
        onClick={handleAsk}
        className="px-4 py-2 bg-green-500 text-white rounded"
      >
        Ask
      </button>
    </div>
  );
}
