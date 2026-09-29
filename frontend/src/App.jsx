import { useState } from "react";
import "./App.css";


const customers = [
  {
    name: "Rahul Sharma",
    initials: "RS",
    tone: "violet",
    scenarios: [
      "My UPI payment is failing again. What should I do?",
      "I'm still having trouble making this payment.",
      "The payment failed again. Do you remember what worked last time?",
    ],
  },
  {
    name: "Priya Mehta",
    initials: "PM",
    tone: "teal",
    scenarios: [
      "My refund still hasn't arrived.",
      "I'm waiting for my refund again. What should I check?",
      "This refund issue is happening again. Do you remember what helped before?",
    ],
  },
  {
    name: "Arjun Patel",
    initials: "AP",
    tone: "coral",
    scenarios: [
      "I can't log in again.",
      "I'm having trouble accessing my account.",
      "My login isn't working. What worked for me last time?",
    ],
  },
];


function getCustomer(customerName) {
  return customers.find(
    (customer) => customer.name === customerName
  );
}


/* =====================================================
   MEMORY TYPE
===================================================== */

function getMemoryType(memory) {

  const text = memory.toLowerCase();


  if (
    text.includes("success") ||
    text.includes("successfully") ||
    text.includes("worked") ||
    text.includes("completed") ||
    text.includes("restored") ||
    text.includes("helped") ||
    text.includes("resolve") ||
    text.includes("resolved")
  ) {

    return {
      label: "Successful solution",
      icon: "✓",
      className: "success",
    };

  }


  if (
    text.includes("prefer") ||
    text.includes("preference")
  ) {

    return {
      label: "Customer preference",
      icon: "♡",
      className: "preference",
    };

  }


  return {
    label: "Previous problem",
    icon: "!",
    className: "problem",
  };
}


/* =====================================================
   SIMPLE MARKDOWN FORMATTER
===================================================== */

function formatMessage(text) {

  if (!text) {
    return null;
  }


  const parts = text.split(
    /(\*\*[^*]+\*\*)/g
  );


  return parts.map(
    (part, index) => {

      if (
        part.startsWith("**") &&
        part.endsWith("**")
      ) {

        return (
          <strong key={index}>
            {part.slice(2, -2)}
          </strong>
        );

      }


      return (
        <span key={index}>
          {part}
        </span>
      );

    }
  );
}


/* =====================================================
   APP
===================================================== */

function App() {

  const [customer, setCustomer] =
    useState("Rahul Sharma");


  const [message, setMessage] =
    useState("");


  const [conversation, setConversation] =
    useState([]);


  const [memories, setMemories] =
    useState([]);


  const [learningActivity, setLearningActivity] =
    useState(null);


  const [loading, setLoading] =
    useState(false);


  const selectedCustomer =
    getCustomer(customer);


  /* =====================================================
     SEND MESSAGE
  ===================================================== */

  async function sendMessage(customMessage = null) {

    const currentMessage =
      (customMessage ?? message).trim();


    if (!currentMessage || loading) {
      return;
    }


    setLoading(true);

    setMessage("");


    setConversation((previous) => [
      ...previous,
      {
        role: "customer",
        text: currentMessage,
        time: new Date().toLocaleTimeString(
          [],
          {
            hour: "2-digit",
            minute: "2-digit",
          }
        ),
      },
    ]);


    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/chat",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              customer_name: customer,
              message: currentMessage,
            }),
          }
        );


      if (!response.ok) {

        throw new Error(
          "Backend request failed"
        );

      }


      const data =
        await response.json();


      setConversation((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.answer || "",
          memories: data.memories || [],
          learningActivity:
            data.learning_activity || null,
          time:
            new Date().toLocaleTimeString(
              [],
              {
                hour: "2-digit",
                minute: "2-digit",
              }
            ),
        },
      ]);


      setMemories(
        data.memories || []
      );


      setLearningActivity(
        data.learning_activity || null
      );


    } catch (error) {

      console.error(error);


      setConversation((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            "I couldn't connect to RecallDesk. Please make sure the FastAPI backend is running.",
          memories: [],
          learningActivity: null,
          error: true,
        },
      ]);

    }


    setLoading(false);
  }


  /* =====================================================
     CUSTOMER CHANGE
  ===================================================== */

  function selectCustomer(newCustomer) {

    setCustomer(newCustomer);

    setConversation([]);

    setMemories([]);

    setLearningActivity(null);

    setMessage("");
  }


  /* =====================================================
     CLEAR
  ===================================================== */

  function clearConversation() {

    setConversation([]);

    setMemories([]);

    setLearningActivity(null);

    setMessage("");
  }


  /* =====================================================
     DEMO SCENARIO
  ===================================================== */

  function runScenario(scenario) {

    sendMessage(scenario);

  }


  const decision =
    learningActivity?.decision_context;


  const recordsRetrieved =
    learningActivity?.raw_memories_found ?? 0;


  const relevantMemories =
    learningActivity?.memories_used ?? 0;


  return (

    <div className="app">


      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>

            <h1>
              RecallDesk
            </h1>

            <p>
              Customer support that remembers.
            </p>

          </div>

        </div>


        {/* HINDSIGHT STATUS */}

        <div className="memory-status">

          <span className="status-dot"></span>

          <span>
            Hindsight Memory Active
          </span>

        </div>

      </header>


      {/* =================================================
          MAIN DASHBOARD
      ================================================= */}

      <main className="dashboard">


        {/* =================================================
            HERO
        ================================================= */}

        <section className="hero">

          <div>

            <span className="hero-label">
              MEMORY-DRIVEN CUSTOMER SUPPORT
            </span>

            <h2>

              Support that gets

              <span>
                smarter with every conversation.
              </span>

            </h2>

            <p>

              RecallDesk remembers previous problems,
              successful solutions and customer preferences,
              then uses that experience to make better
              decisions next time.

            </p>

          </div>


          <div className="hero-stats">

            <div className="hero-stat">

              <strong>
                {recordsRetrieved || "—"}
              </strong>

              <span>
                Hindsight records
              </span>

            </div>


            <div className="hero-stat green">

              <strong>
                {learningActivity
                  ? "✓"
                  : "—"}
              </strong>

              <span>
                Learning status
              </span>

            </div>

          </div>

        </section>


        {/* =================================================
            CUSTOMER SELECTOR
        ================================================= */}

        <section className="customer-selector-bar">

          <div className="customer-title">

            <span>
              ◉
            </span>

            Customer

          </div>


          <div className="customer-options">

            {customers.map(
              (item) => (

                <button
                  key={item.name}
                  className={
                    customer === item.name
                      ? "customer-option active"
                      : "customer-option"
                  }
                  onClick={() =>
                    selectCustomer(
                      item.name
                    )
                  }
                >

                  <span
                    className={
                      `customer-avatar ${item.tone}`
                    }
                  >
                    {item.initials}
                  </span>


                  <span className="customer-info">

                    <strong>
                      {item.name}
                    </strong>

                    <small>
                      Returning customer
                    </small>

                  </span>


                  {customer === item.name && (

                    <span className="check">
                      ✓
                    </span>

                  )}

                </button>

              )
            )}

          </div>

        </section>


        {/* =================================================
            WORKSPACE
        ================================================= */}

        <section className="workspace">


          {/* =================================================
              CHAT PANEL
          ================================================= */}

          <section className="chat-panel">


            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  CUSTOMER CONVERSATION
                </span>

                <h3>
                  Support workspace
                </h3>

              </div>


              <div className="live-badge">

                <span></span>

                Live

              </div>

            </div>


            {/* =================================================
                DEMO SCENARIOS
            ================================================= */}

            <div className="demo-area">

              <div className="demo-heading">

                <div>

                  <strong>
                    Demo scenarios
                  </strong>

                  <span>
                    Quick prompts for your presentation
                  </span>

                </div>


                {conversation.length > 0 && (

                  <button
                    className="clear-button"
                    onClick={clearConversation}
                  >
                    Clear
                  </button>

                )}

              </div>


              <div className="scenario-buttons">

                {selectedCustomer?.scenarios.map(
                  (scenario, index) => (

                    <button
                      key={scenario}
                      className="scenario-button"
                      onClick={() =>
                        runScenario(
                          scenario
                        )
                      }
                      disabled={loading}
                    >

                      <span>
                        {index + 1}
                      </span>

                      {scenario}

                    </button>

                  )
                )}

              </div>

            </div>


            {/* =================================================
                CONVERSATION
            ================================================= */}

            <div className="conversation">

              {conversation.length === 0 ? (

                <div className="conversation-empty">

                  <div className="empty-icon">
                    ✦
                  </div>

                  <strong>
                    Ready to remember
                  </strong>

                  <p>
                    Choose a demo scenario above or
                    describe a customer issue below.
                  </p>

                  <div className="memory-flow">

                    <span>
                      Recall
                    </span>

                    <i>
                      →
                    </i>

                    <span>
                      Reason
                    </span>

                    <i>
                      →
                    </i>

                    <span>
                      Learn
                    </span>

                  </div>

                </div>

              ) : (

                conversation.map(
                  (item, index) => (

                    <div
                      key={index}
                      className={
                        item.role ===
                        "customer"
                          ? "message customer-message"
                          : "message assistant-message"
                      }
                    >

                      <div className="message-label">

                        <span
                          className={
                            item.role ===
                            "customer"
                              ? "avatar customer-avatar"
                              : "avatar"
                          }
                        >

                          {item.role ===
                          "customer"
                            ? selectedCustomer?.initials
                            : "R"}

                        </span>


                        <strong>

                          {item.role ===
                          "customer"
                            ? customer
                            : "RecallDesk"}

                        </strong>


                        {item.time && (

                          <small>
                            {item.time}
                          </small>

                        )}

                      </div>


                      <p>
                        {item.role === "assistant"
                          ? formatMessage(item.text)
                          : item.text}
                      </p>


                      {item.role ===
                        "assistant" &&
                        item.memories?.length >
                          0 && (

                        <div className="response-memory">

                          <div className="response-memory-title">

                            <span>
                              ✦
                            </span>

                            Memory influenced this response

                          </div>


                          <p>
                            RecallDesk used previous
                            customer experience to
                            personalize this recommendation.
                          </p>

                        </div>

                      )}

                    </div>

                  )
                )

              )}


              {loading && (

                <div className="thinking-card">

                  <span>
                    ✦
                  </span>

                  <div>

                    <strong>
                      Recalling previous experience
                    </strong>

                    <div className="dots">

                      <i></i>
                      <i></i>
                      <i></i>

                    </div>

                  </div>

                </div>

              )}

            </div>


            {/* =================================================
                INPUT
            ================================================= */}

            <div className="input-area">

              <input
                type="text"
                value={message}
                placeholder={
                  `Type a message from ${customer}...`
                }
                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }
                onKeyDown={(event) => {

                  if (
                    event.key ===
                    "Enter"
                  ) {

                    sendMessage();

                  }

                }}
              />


              <button
                onClick={() =>
                  sendMessage()
                }
                disabled={
                  loading ||
                  !message.trim()
                }
              >

                {loading
                  ? "..."
                  : "Send"}

                {!loading && (

                  <span>
                    →
                  </span>

                )}

              </button>

            </div>

          </section>


          {/* =================================================
              MEMORY PANEL
          ================================================= */}

          <aside className="memory-panel">


            <div className="memory-panel-heading">

              <div>

                <span className="panel-label">
                  HINDSIGHT
                </span>

                <h3>
                  Memory engine
                </h3>

                <p>
                  Relevant past experiences,
                  right when they are needed.
                </p>

              </div>


              <div className="memory-symbol">
                ✦
              </div>

            </div>


            {/* MEMORY STATS */}

            <div className="memory-stats">

              <div>

                <strong>
                  {recordsRetrieved || "—"}
                </strong>

                <span>
                  records retrieved
                </span>

              </div>


              <div>

                <strong>
                  {relevantMemories || "—"}
                </strong>

                <span>
                  relevant insights
                </span>

              </div>

            </div>


            {/* =================================================
                MEMORY → DECISION
            ================================================= */}

            {decision ? (

              <div className="decision-section">

                <div className="decision-title">

                  <strong>
                    Memory
                  </strong>

                  <span>
                    →
                  </span>

                  <strong>
                    Decision
                  </strong>

                </div>


                <p className="decision-description">

                  How Hindsight memory influenced
                  RecallDesk's decision.

                </p>


                <div className="timeline">


                  {/* STEP 1 */}

                  <div className="timeline-item">

                    <div className="timeline-number pink">
                      01
                    </div>


                    <div className="timeline-card">

                      <span>
                        PAST EXPERIENCE
                      </span>

                      <strong>
                        {decision.previous_problem}
                      </strong>

                      <small>
                        Retrieved from Hindsight memory.
                      </small>

                    </div>

                  </div>


                  <div className="timeline-line"></div>


                  {/* STEP 2 */}

                  <div className="timeline-item">

                    <div className="timeline-number green">
                      02
                    </div>


                    <div className="timeline-card">

                      <span>
                        SUCCESSFUL OUTCOME
                      </span>

                      <strong>
                        {decision.successful_outcome}
                      </strong>

                      <small>
                        A previous outcome that influenced
                        the recommendation.
                      </small>

                    </div>

                  </div>


                  <div className="timeline-line"></div>


                  {/* STEP 3 */}

                  <div className="timeline-item">

                    <div className="timeline-number orange">
                      03
                    </div>


                    <div className="timeline-card">

                      <span>
                        CURRENT ISSUE
                      </span>

                      <strong>
                        {decision.current_issue}
                      </strong>

                      <small>
                        The current issue was compared
                        with previous experience.
                      </small>

                    </div>

                  </div>


                  <div className="timeline-line"></div>


                  {/* STEP 4 */}

                  <div className="timeline-item">

                    <div className="timeline-number purple">
                      ✓
                    </div>


                    <div className="timeline-card final">

                      <span>
                        MEMORY-INFORMED DECISION
                      </span>

                      <strong>
                        {decision.decision}
                      </strong>

                      <small>
                        The decision is based on {customer}'s
                        own previous experience.
                      </small>

                    </div>

                  </div>

                </div>

              </div>

            ) : (

              <div className="memory-waiting">

                <div className="waiting-icon">
                  ◎
                </div>

                <strong>
                  Waiting for memory...
                </strong>

                <p>
                  Send a message to see how
                  previous customer experience
                  influences the decision.
                </p>

                <div className="waiting-flow">

                  <span>
                    Recall
                  </span>

                  <i>
                    →
                  </i>

                  <span>
                    Decision
                  </span>

                  <i>
                    →
                  </i>

                  <span>
                    Store
                  </span>

                </div>

              </div>

            )}


            {/* =================================================
                RETRIEVED MEMORIES
            ================================================= */}

            <div className="retrieved-section">

              <div className="retrieved-heading">

                <strong>
                  Retrieved Memory Insights
                </strong>

                <span>
                  {memories.length}
                </span>

              </div>


              {memories.length > 0 ? (

                <div className="retrieved-list">

                  {memories
                    .slice(0, 4)
                    .map(
                      (memory, index) => {

                        const type =
                          getMemoryType(
                            memory
                          );


                        return (

                          <div
                            className="retrieved-memory"
                            key={index}
                          >

                            <div
                              className={
                                `memory-marker ${type.className}`
                              }
                            >
                              {type.icon}
                            </div>


                            <div>

                              <span>
                                {type.label}
                              </span>

                              <p>
                                {memory}
                              </p>

                            </div>

                          </div>

                        );

                      }
                    )}

                </div>

              ) : (

                <p className="no-memory-text">

                  Relevant customer memories will
                  appear here after a message is sent.

                </p>

              )}

            </div>

          </aside>

        </section>


        {/* =================================================
            LEARNING ACTIVITY
        ================================================= */}

        <section className="learning-bar">

          <div className="learning-title">

            <div className="learning-icon">
              ✦
            </div>

            <div>

              <strong>
                Learning Activity
              </strong>

              <span>
                Every interaction becomes useful context.
              </span>

            </div>

          </div>


          <div className="learning-metrics">

            <div className="learning-metric">

              <span>
                {recordsRetrieved}
              </span>

              <div>

                <strong>
                  Hindsight records
                </strong>

                <small>
                  Retrieved for this request
                </small>

              </div>

            </div>


            <div className="learning-metric">

              <span className="teal">
                {relevantMemories}
              </span>

              <div>

                <strong>
                  Relevant memories
                </strong>

                <small>
                  Used in reasoning
                </small>

              </div>

            </div>


            <div className="learning-metric">

              <span className="green">

                {learningActivity
                  ? "✓"
                  : "○"}

              </span>

              <div>

                <strong>

                  {learningActivity
                    ? "Stored"
                    : "Waiting"}

                </strong>

                <small>
                  New interaction
                </small>

              </div>

            </div>

          </div>


          <div className="learning-explanation">

            <strong>
              Hindsight loop
            </strong>

            <p>

              Recall previous experience →
              use it for the decision →
              store the new interaction for future support.

            </p>

          </div>

        </section>

      </main>

    </div>

  );

}


export default App;