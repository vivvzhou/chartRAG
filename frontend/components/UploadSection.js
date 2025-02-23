// frontend/components/UploadSection.js
"use client";

import { useState } from "react";

export default function UploadSection({ summary, setSummary }) {
  const [file, setFile] = useState(null);

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

  return (
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
          <p className="whitespace-pre-wrap">{summary}</p>
        </div>
      )}
    </div>
  );
}
