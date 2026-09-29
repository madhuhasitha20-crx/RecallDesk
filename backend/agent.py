import os
from dotenv import load_dotenv
from groq import Groq

from memory import recall_customer, remember_customer


load_dotenv()


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_demo_memories(customer_name, memories):

    text = " ".join(memories).lower()

    demo_memories = []

    # -----------------------------------------
    # RAHUL SHARMA
    # -----------------------------------------

    if customer_name.lower() == "rahul sharma":

        if (
            "upi" in text
            and (
                "fail" in text
                or "failure" in text
                or "failed" in text
            )
        ):
            demo_memories.append(
                "Rahul previously experienced repeated UPI payment failures."
            )

        if (
            "card" in text
            and (
                "success" in text
                or "successfully" in text
                or "completed" in text
                or "worked" in text
                or "using a card" in text
                or "card payment" in text
            )
        ):
            demo_memories.append(
                "Rahul successfully completed a payment using a card after UPI failed."
            )

        if (
            "prefer" in text
            and "email" in text
        ):
            demo_memories.append(
                "Rahul prefers important support communication by email."
            )

    # -----------------------------------------
    # PRIYA MEHTA
    # -----------------------------------------

    elif customer_name.lower() == "priya mehta":

        if "refund" in text:
            demo_memories.append(
                "Priya previously experienced a delayed refund."
            )

        if "order history" in text:
            demo_memories.append(
                "Checking order history helped Priya resolve a previous refund issue."
            )

        if (
            "prefer" in text
            and "email" in text
        ):
            demo_memories.append(
                "Priya prefers important support updates by email."
            )

    # -----------------------------------------
    # ARJUN PATEL
    # -----------------------------------------

    elif customer_name.lower() == "arjun patel":

        if (
            "login" in text
            or "password" in text
        ):
            demo_memories.append(
                "Arjun previously experienced a login problem caused by an expired password."
            )

        if (
            "reset" in text
            or "success" in text
            or "successfully" in text
        ):
            demo_memories.append(
                "Arjun successfully regained access using the password reset flow."
            )

        if (
            "prefer" in text
            and "quick" in text
        ):
            demo_memories.append(
                "Arjun prefers quick troubleshooting steps."
            )

    # -----------------------------------------
    # GENERIC FALLBACK
    # -----------------------------------------

    if not demo_memories:

        for memory in memories[:3]:

            clean = memory.strip()

            if clean:
                demo_memories.append(clean)

    return demo_memories[:4]


def build_decision_context(
    customer_name,
    customer_message,
    memories
):

    text = " ".join(memories).lower()

    customer = customer_name.lower()

    # -----------------------------------------
    # RAHUL DECISION
    # -----------------------------------------

    if customer == "rahul sharma":

        if "upi" in text:

            previous_problem = (
                "UPI payment failed previously"
            )

        else:

            previous_problem = (
                "Previous payment problem"
            )

        if (
            "card" in text
            or "using a card" in text
        ):

            successful_outcome = (
                "Card payment successfully completed the transaction"
            )

        else:

            successful_outcome = (
                "A previous payment solution worked"
            )

        if "upi" in customer_message.lower():

            current_issue = (
                "UPI payment is failing again"
            )

        else:

            current_issue = customer_message

        if (
            "card" in text
            or "using a card" in text
        ):

            decision = (
                "Recommend card payment based on Rahul's previous success"
            )

        else:

            decision = (
                "Use Rahul's previous payment experience"
            )

        return {
            "previous_problem": previous_problem,
            "successful_outcome": successful_outcome,
            "current_issue": current_issue,
            "decision": decision,
        }

    # -----------------------------------------
    # PRIYA DECISION
    # -----------------------------------------

    if customer == "priya mehta":

        if "refund" in text:

            previous_problem = (
                "Refund was delayed previously"
            )

        else:

            previous_problem = (
                "Previous refund issue"
            )

        if "order history" in text:

            successful_outcome = (
                "Checking order history helped"
            )

        else:

            successful_outcome = (
                "Previous refund troubleshooting helped"
            )

        current_issue = customer_message

        decision = (
            "Recommend checking refund status through order history"
        )

        return {
            "previous_problem": previous_problem,
            "successful_outcome": successful_outcome,
            "current_issue": current_issue,
            "decision": decision,
        }

    # -----------------------------------------
    # ARJUN DECISION
    # -----------------------------------------

    if customer == "arjun patel":

        if (
            "password" in text
            or "login" in text
        ):

            previous_problem = (
                "Password expired and caused a login problem"
            )

        else:

            previous_problem = (
                "Previous login problem"
            )

        if "reset" in text:

            successful_outcome = (
                "Password reset successfully restored access"
            )

        else:

            successful_outcome = (
                "Previous troubleshooting restored access"
            )

        current_issue = customer_message

        decision = (
            "Recommend the password reset flow"
        )

        return {
            "previous_problem": previous_problem,
            "successful_outcome": successful_outcome,
            "current_issue": current_issue,
            "decision": decision,
        }

    # -----------------------------------------
    # GENERIC
    # -----------------------------------------

    return {
        "previous_problem": (
            "Previous customer support issue"
        ),
        "successful_outcome": (
            "A previous solution was identified"
        ),
        "current_issue": customer_message,
        "decision": (
            "Use relevant previous customer experience"
        ),
    }


def support_customer(
    customer_message,
    customer_name
):

    # -----------------------------------------
    # HINDSIGHT RECALL
    # -----------------------------------------

    memories = recall_customer(
        f"""
        CUSTOMER: {customer_name}

        Retrieve the most relevant memories belonging ONLY
        to this customer.

        Current customer request:
        {customer_message}

        Retrieve related memories even if they describe
        different parts of the same previous support journey.

        Prioritize:

        - previous problems
        - failed attempts
        - successful solutions
        - what worked
        - customer preferences
        - previous support outcomes
        - recent interactions
        - newly learned information

        IMPORTANT:
        Return memories from {customer_name} only.
        Do not return memories from other customers.
        """
    )

    # -----------------------------------------
    # CUSTOMER FILTER
    # -----------------------------------------

    customer_name_lower = customer_name.lower()

    customer_memories = []

    for memory in memories:

        if customer_name_lower in memory.lower():

            customer_memories.append(
                memory.strip()
            )

    # -----------------------------------------
    # EXACT DUPLICATE REMOVAL
    # -----------------------------------------

    unique_raw_memories = []

    seen = set()

    for memory in customer_memories:

        key = memory.lower().strip()

        if key not in seen:

            seen.add(key)

            unique_raw_memories.append(
                memory
            )

    # Keep enough history for Hindsight context
    unique_raw_memories = unique_raw_memories[:12]

    # -----------------------------------------
    # MEMORY TEXT
    # -----------------------------------------

    memory_text = " ".join(
        unique_raw_memories
    ).lower()

    # -----------------------------------------
    # LEARNED EXPERIENCE
    # -----------------------------------------

    learned_solution = ""

    if (
        customer_name_lower == "rahul sharma"
        and "upi" in memory_text
        and (
            "card" in memory_text
            or "using a card" in memory_text
        )
    ):

        learned_solution = """
Rahul previously experienced UPI payment failures
and successfully completed a payment using a card.

The previous successful card payment should influence
the recommendation if Rahul reports another payment issue.
"""

    elif (
        customer_name_lower == "priya mehta"
        and "refund" in memory_text
    ):

        learned_solution = """
Priya previously experienced a delayed refund.

Checking the refund status through order history
was useful in resolving the previous issue.
"""

    elif (
        customer_name_lower == "arjun patel"
        and (
            "login" in memory_text
            or "password" in memory_text
        )
    ):

        learned_solution = """
Arjun previously had a login problem caused by
an expired password.

He successfully regained access using the
password reset flow.
"""

    else:

        learned_solution = """
No specific successful previous solution was confidently
identified for this customer.

Use only the available customer history.
Do not invent facts.
"""

    # -----------------------------------------
    # MEMORY CONTEXT FOR LLM
    # -----------------------------------------

    if unique_raw_memories:

        memory_context = "\n".join(
            f"- {memory}"
            for memory in unique_raw_memories
        )

    else:

        memory_context = (
            "No previous memories found for this customer."
        )

    # -----------------------------------------
    # LLM RESPONSE
    # -----------------------------------------

    prompt = f"""
You are RecallDesk, an AI customer-support agent
that learns from previous customer experiences.

Customer:
{customer_name}

Current customer message:
{customer_message}

Previous memories belonging ONLY to {customer_name}:
{memory_context}

IMPORTANT LEARNED EXPERIENCE:
{learned_solution}

Instructions:

- Respond specifically to {customer_name}.
- Use only this customer's history.
- Never use another customer's information.
- If a previous successful solution is relevant,
  use that experience in your recommendation.
- Briefly explain that the recommendation is based
  on the customer's previous experience.
- Do not invent facts.
- Do not claim to perform external actions.
- Do not claim to have access to orders, accounts,
  payment systems, email, tickets, databases, or
  other external systems unless that access is explicitly
  provided in the conversation.
- Do not say that you will send an email.
- Do not say that you will investigate or update an
  external record.
- Do not offer actions that RecallDesk cannot actually perform.
- Do not add unnecessary generic troubleshooting.
- Keep the response concise: usually 2 to 4 sentences.
- If simple troubleshooting steps are necessary,
  keep them short and directly relevant.
- Make the memory-based recommendation clear.
- Answer the actual current issue.

Return only the customer-support response.
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    # -----------------------------------------
    # STORE NEW INTERACTION
    # -----------------------------------------

    new_memory = f"""
Customer: {customer_name}

New support interaction:

Customer reported:
{customer_message}

RecallDesk response:
{answer}

Previous experience used:
{learned_solution}

This interaction should be remembered for future
support conversations.
"""

    remember_customer(new_memory)

    # -----------------------------------------
    # CLEAN DEMO MEMORIES
    # -----------------------------------------

    demo_memories = build_demo_memories(
        customer_name,
        unique_raw_memories
    )

    # -----------------------------------------
    # DECISION CONTEXT
    # -----------------------------------------

    decision_context = build_decision_context(
        customer_name,
        customer_message,
        unique_raw_memories
    )

    # -----------------------------------------
    # LEARNING ACTIVITY
    # -----------------------------------------

    learning_activity = {

        "customer": customer_name,

        "new_issue": customer_message,

        "memories_used": len(demo_memories),

        "raw_memories_found": len(
            unique_raw_memories
        ),

        "learned_solution":
            learned_solution.strip(),

        "memory_created": True,

        "decision_context": decision_context,

        "message": (
            f"RecallDesk retrieved "
            f"{len(unique_raw_memories)} Hindsight "
            f"memory records, identified the relevant "
            f"customer experience, and stored this new "
            f"interaction for future support."
        )
    }

    return (
        answer,
        demo_memories,
        learning_activity
    )