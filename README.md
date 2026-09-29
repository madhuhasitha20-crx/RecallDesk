# RecallDesk

### AI Customer Support That Remembers

RecallDesk is an AI-powered customer-support agent that remembers previous customer interactions, learns from successful and unsuccessful support experiences, and uses that knowledge to provide more personalized support in future conversations.

Instead of treating every support conversation as a new interaction, RecallDesk uses persistent memory to understand what happened before, what worked, what failed, and what the customer prefers.

---

## 🎯 Problem

Traditional customer-support systems often treat each interaction independently.

Even when previous conversations are stored, simply retrieving old information does not guarantee that it will influence the next decision.

For example:

A customer may have experienced repeated UPI payment failures and later successfully completed the payment using a card.

If the same customer returns with another payment problem, an effective support agent should recognize that previous experience and use it when deciding what to recommend.

---

## 💡 Solution

RecallDesk combines an LLM with persistent memory to create a support experience that improves across conversations.

The system:

1. Receives the customer's current issue.
2. Retrieves relevant previous experiences.
3. Identifies previous problems and successful outcomes.
4. Uses that experience to influence the current recommendation.
5. Generates a personalized support response.
6. Stores the new interaction for future conversations.

The goal is not simply to remember information.

The goal is to **use memory to make better support decisions.**

---

## 🧠 Hindsight Memory

Hindsight is the core memory layer of RecallDesk.

RecallDesk uses Hindsight to:

- Store customer support interactions.
- Retrieve relevant previous experiences.
- Connect current problems with previous problems.
- Recall successful solutions.
- Preserve customer preferences.
- Store new interactions for future support.

The memory loop is:

```text
Recall → Reason → Decide → Store
   ↑                    |
   └────────────────────┘
🔥 What Makes RecallDesk Different

RecallDesk does not treat memory as a simple chat-history feature.

It focuses on experience-based support.

For example:

Previous experience
        ↓
UPI payment failed
        ↓
Customer tried card payment
        ↓
Card payment succeeded
        ↓
Customer returns with another payment problem
        ↓
Hindsight recalls the previous experience
        ↓
RecallDesk recommends the previously successful approach

The previous experience directly influences the current decision.

✨ Key Features
Persistent Customer Memory

RecallDesk stores previous customer interactions and retrieves them when relevant.

Experience-Based Recommendations

The system considers previous failed attempts and successful solutions before responding.

Customer-Specific Memory

Customer experiences are kept separate so that one customer's history is not incorrectly used for another customer.

Memory → Decision Visualization

The interface shows:

Past experience
Successful outcome
Current issue
Memory-informed decision

This makes the role of memory transparent.

Continuous Learning Loop

Each new interaction is stored so it can become useful context in future support conversations.

🏗️ Architecture
                    ┌─────────────────────┐
                    │      Customer       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     React UI        │
                    │   Support Workspace │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │     Python Agent    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ Hindsight Recall │   │     Groq LLM     │
          │ Persistent Memory│   │ Response Engine  │
          └────────┬─────────┘   └────────┬─────────┘
                   │                      │
                   └──────────┬───────────┘
                              │
                              ▼
                   Personalized Response
                              │
                              ▼
                    Hindsight Retain
                              │
                              ▼
                    Future Conversations
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
AI
Groq
openai/gpt-oss-120b
Memory
Hindsight
Hindsight Python SDK
📁 Project Structure
RecallDesk/
│
├── backend/
│   ├── agent.py
│   ├── main.py
│   ├── memory.py
│   └── test_agent.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── clear_memory.py
├── seed_memory.py
├── test_hindsight.py
├── .gitignore
└── README.md
🚀 Running the Project Locally
1. Clone the repository
git clone https://github.com/madhuhasitha20-crx/RecallDesk.git
cd RecallDesk
2. Backend setup

Create and activate a Python virtual environment.

python -m venv venv

Windows:

venv\Scripts\activate

Install the required Python packages:

pip install hindsight-client python-dotenv groq fastapi uvicorn
3. Environment variables

Create a .env file inside the project root.

HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=recalldesk
GROQ_API_KEY=your_groq_api_key

Never commit .env or expose API keys publicly.

4. Start the backend
cd backend
uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000
5. Start the frontend

Open another terminal:

cd frontend
npm install
npm run dev

The frontend will normally run at:

http://localhost:5174
🧪 Example Demo
Customer

Rahul Sharma

First interaction

My UPI payment is failing again. What should I do?

RecallDesk retrieves Rahul's previous support experience.

The system identifies:

Previous UPI payment failures
Successful card payment

The interaction is then stored for future support.

Returning interaction

The payment failed again. Do you remember what worked last time?

RecallDesk retrieves the relevant history and recommends the previously successful card-payment approach.

The interface visualizes the reasoning:

PAST EXPERIENCE
UPI payment failed previously

        ↓

SUCCESSFUL OUTCOME
Card payment successfully completed

        ↓

CURRENT ISSUE
Payment failed again

        ↓

MEMORY-INFORMED DECISION
Recommend card payment based on previous success
🔄 Memory Loop

RecallDesk continuously follows this cycle:

1. Recall

Retrieve relevant customer experiences from Hindsight.

2. Reason

Compare the current issue with previous experiences.

3. Decide

Use successful previous outcomes and relevant preferences to influence the response.

4. Store

Save the new interaction so future conversations can benefit from it.

┌──────────┐
│  Recall  │
└────┬─────┘
     ↓
┌──────────┐
│  Reason  │
└────┬─────┘
     ↓
┌──────────┐
│  Decide  │
└────┬─────┘
     ↓
┌──────────┐
│  Store   │
└────┬─────┘
     │
     └──────────────→ Future Recall
🔐 Security

API keys and environment variables are intentionally excluded from the repository.

The project uses .gitignore to prevent sensitive configuration such as:

.env

from being committed.

🎥 Demo

Demo video:

Coming soon

🌱 Future Improvements

Potential future extensions include:

Larger customer-support datasets
Automatic ticket categorization
More support channels
Agent analytics
Feedback-based memory refinement
Additional customer preferences
Production authentication and deployment
👥 Project

RecallDesk

AI customer support powered by persistent memory.

Built with React, FastAPI, Groq, and Hindsight.


### Step 2

After pasting:

Scroll to the bottom → click **Commit changes**.

For the commit message, use:

```text
Improve RecallDesk documentation
