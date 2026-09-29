from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import support_customer


app = FastAPI(title="RecallDesk API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    customer_name: str
    message: str


@app.get("/")
def home():
    return {
        "message": "RecallDesk API is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer, memories, learning_activity = support_customer(
        customer_message=request.message,
        customer_name=request.customer_name
    )

    # -----------------------------------------
    # REMOVE DUPLICATE MEMORIES
    # -----------------------------------------

    unique_memories = []
    seen = set()

    for memory in memories:
        clean_memory = memory.strip()
        key = clean_memory.lower()

        if key not in seen:
            seen.add(key)
            unique_memories.append(clean_memory)

    unique_memories = unique_memories[:6]

    return {
        "customer_name": request.customer_name,
        "message": request.message,
        "answer": answer,
        "memories": unique_memories,
        "learning_activity": learning_activity
    } 