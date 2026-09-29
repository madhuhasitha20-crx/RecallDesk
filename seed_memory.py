import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

memories = [

    # =========================
    # RAHUL SHARMA
    # =========================

    """
    Customer: Rahul Sharma.

    Rahul's UPI payment failed twice.
    """,

    """
    Customer: Rahul Sharma.

    Rahul successfully completed a payment using a card after
    the UPI failures.
    """,

    """
    Customer: Rahul Sharma.

    Rahul prefers email communication.
    """,

    """
    Customer: Rahul Sharma.

    Rahul uses an Android 14 device.
    """,

    # =========================
    # PRIYA MEHTA
    # =========================

    """
    Customer: Priya Mehta.

    Priya previously had an issue with a delayed refund.
    The refund appeared after approximately three business days.
    """,

    """
    Customer: Priya Mehta.

    Priya successfully resolved a refund issue after checking
    the refund status from the order history page.
    """,

    """
    Customer: Priya Mehta.

    Priya prefers receiving important support updates by email.
    """,

    """
    Customer: Priya Mehta.

    Priya usually checks her order history before contacting
    support about refund-related issues.
    """,

    # =========================
    # ARJUN PATEL
    # =========================

    """
    Customer: Arjun Patel.

    Arjun previously experienced a login problem because his
    password had expired.
    """,

    """
    Customer: Arjun Patel.

    Arjun successfully regained access after resetting his
    password through the password reset flow.
    """,

    """
    Customer: Arjun Patel.

    Arjun prefers quick troubleshooting steps rather than
    lengthy explanations.
    """,

    """
    Customer: Arjun Patel.

    Arjun uses a Windows laptop when accessing the support portal.
    """
]

for memory in memories:
    client.retain(
        bank_id=BANK_ID,
        content=memory
    )

print("✅ Rahul, Priya, and Arjun customer histories stored!")

client.close()