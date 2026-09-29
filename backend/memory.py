import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


def remember_customer(content):
    """Store a customer interaction in Hindsight."""
    
    client.retain(
        bank_id=BANK_ID,
        content=content
    )


def recall_customer(query):
    """Retrieve relevant customer memories from Hindsight."""
    
    result = client.recall(
        bank_id=BANK_ID,
        query=query
    )

    memories = []

    for memory in result.results:
        memories.append(memory.text)

    return memories
def close_memory_client():
    client.close()