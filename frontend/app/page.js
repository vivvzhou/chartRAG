"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [userMessage, setUserMessage] = useState("");
  const [backendResponse, setBackendResponse] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("datafile", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        // Assuming the backend returns a summary in the flash message
        const data = await response.json();
        setSummary(data.summary || "File uploaded successfully.");
      } else {
        const data = await response.json();
        alert(data.error || "Error uploading file.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while uploading the file.");
    }
  };

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
    <div className="container mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Data Analyzer</h1>
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Upload CSV File</h2>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Upload
        </button>
        {summary && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Summary:</h3>
            <p>{summary}</p>
          </div>
        )}
      </div>
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
        {answer && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Answer:</h3>
            <p>{answer}</p>
          </div>
        )}
      </div>
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
        {backendResponse && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Response:</h3>
            <p>{backendResponse}</p>
          </div>
        )}
      </div>
    </div>
  );
}
