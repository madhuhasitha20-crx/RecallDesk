import { useState } from "react";
import "./App.css";

function getMemoryType(memory) {
  const text = memory.toLowerCase();

  if (
    text.includes("success") ||
    text.includes("successfully") ||
    text.includes("worked") ||
    text.includes("completed")
  ) {
    return "🟢 Successful solution";
  }

  if (text.includes("prefer")) {
    return "📧 Customer preference";
  }

  if (
    text.includes("recommend") ||
    text.includes("recommended") ||
    text.includes("learning")
  ) {
    return "🧠 Learning applied";
  }

  return "🔴 Previous problem";
}

function App() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          customer_name: "Rahul Sharma",
          message: message,
        }),
      });

      const data = await response.json();

      setAnswer(data.answer);
      setMemories(data.memories);
      setMessage("");
    } catch (error) {
      console.error(error);
      setAnswer("Could not connect to RecallDesk backend.");
    }

    setLoading(false);
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>RecallDesk</h1>
          <p>Customer support that remembers.</p>
        </div>

        <div className="memory-status">
          <span className="status-dot"></span>
          Hindsight Memory Active
        </div>
      </header>

      <main className="dashboard">

        <section className="chat-panel">
          <h2>Customer Support</h2>
          <p>Rahul Sharma</p>

          <div className="conversation">

            <div className="message">
              <strong>RecallDesk</strong>
              <p>
                Hello Rahul! I remember your previous support experiences.
              </p>
            </div>

            {answer && (
              <div className="message">
                <strong>Rahul</strong>
                <p>{message || "My payment is failing again."}</p>
              </div>
            )}

            {answer && (
              <div className="message">
                <strong>RecallDesk</strong>
                <p>{answer}</p>
              </div>
            )}

            {answer && memories.length > 0 && (
              <div className="memory-impact">
                <strong>🧠 Memory influenced this response</strong>

                <p>
                  RecallDesk used previous customer experiences to
                  personalize this recommendation.
                </p>

                {memories.slice(0, 3).map((memory, index) => (
                  <div className="impact-item" key={index}>
                    <span>{getMemoryType(memory)}</span>
                    <strong>{memory}</strong>
                  </div>
                ))}
              </div>
            )}

            {loading && (
              <div className="message">
                <strong>RecallDesk</strong>
                <p>Thinking and recalling previous experiences...</p>
              </div>
            )}

          </div>

          <div className="input-area">
            <input
              type="text"
              placeholder="Type a customer message..."
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage} disabled={loading}>
              {loading ? "Thinking..." : "Send"}
            </button>
          </div>
        </section>

        <aside className="memory-panel">
          <h2>Memory Timeline</h2>
          <p>What RecallDesk remembers</p>

          {memories.length === 0 ? (
            <div className="memory-item">
              <strong>Waiting for memory...</strong>
              <p>
                Send a message to retrieve relevant customer memories.
              </p>
            </div>
          ) : (
            memories.slice(0, 6).map((memory, index) => (
              <div className="memory-item" key={index}>
                <strong>{getMemoryType(memory)}</strong>
                <p>{memory}</p>
              </div>
            ))
          )}
        </aside>

      </main>
    </div>
  );
}

export default App;