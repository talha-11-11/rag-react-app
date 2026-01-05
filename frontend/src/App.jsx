import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setLoading(true);

    try {
      const response = await fetch("https://rag-backend.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Error: Could not reach backend server",
        },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div
      style={{
        maxWidth: 800,
        margin: "40px auto",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h2>🔎 Website Knowledge Chat (RAG)</h2>

      <div
        style={{
          border: "1px solid #ccc",
          padding: 12,
          minHeight: 300,
          marginBottom: 12,
          background: "#fafafa",
        }}
      >
        {messages.map((msg, idx) => (
          <p key={idx}>
            <strong>{msg.role === "user" ? "You" : "AI"}:</strong>{" "}
            {msg.content}
          </p>
        ))}

        {loading && <p><i>AI is thinking...</i></p>}
      </div>

      <textarea
        rows={3}
        style={{ width: "100%", padding: 8 }}
        placeholder="Ask something about the websites..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button
        onClick={askAI}
        style={{ marginTop: 10, padding: "8px 16px" }}
      >
        Ask
      </button>
    </div>
  );
}

export default App;
