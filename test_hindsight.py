import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load .env
load_dotenv()

# Connect to Hindsight
client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

print("✅ Connected to Hindsight!")

# Store a customer memory
client.retain(
    bank_id=BANK_ID,
    content="""
    Customer Rahul Sharma uses an Android 14 phone.
    Rahul's UPI payment failed twice.
    Support previously suggested paying by card.
    The card payment succeeded.
    Rahul prefers email communication.
    """
)

print("✅ Customer memory stored!")

# Ask Hindsight to recall it
result = client.recall(
    bank_id=BANK_ID,
    query="What happened with Rahul Sharma's previous payment problem?"
)

print("\n--- RECALLED MEMORY ---")

for memory in result.results:
    print("-", memory.text)

client.close()