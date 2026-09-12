from google.adk.agents import Agent
from google.adk.apps import App


def get_kyc_requirements(customer_type: str) -> dict:
    """Return synthetic KYC document requirements for a customer type."""

    requirements = {
        "individual": [
            "government-issued photo ID",
            "proof of address",
            "tax identification document",
        ],
        "business": [
            "business registration document",
            "tax identification document",
            "registered business address proof",
            "authorized representative identification",
        ],
    }

    normalized_type = customer_type.strip().lower()

    if normalized_type not in requirements:
        return {
            "status": "unsupported_customer_type",
            "customer_type": normalized_type,
            "supported_types": list(requirements.keys()),
        }

    return {
        "status": "success",
        "customer_type": normalized_type,
        "documents": requirements[normalized_type],
        "data_source": "synthetic_demo_policy",
    }


root_agent = Agent(
    name="banking_servicing_agent",
    model="gemini-3.6-flash",
    description="AI assistant for synthetic banking servicing workflows.",
    instruction="""
    You are an AI assistant for a synthetic banking servicing platform.

    Your current responsibility is to answer KYC document requirement questions
    using the available tools.

    Rules:
    - Use tools for authoritative synthetic banking information.
    - When answering from a tool result, use only facts explicitly returned by the tool.
    - Do not add examples, requirements, or policy details from your own knowledge.
    - Do not invent customer information.
    - Do not claim access to real banking systems.
    - All customer and policy information in this project is synthetic.
    - If a tool cannot answer the request, say so clearly.
    """,
    tools=[get_kyc_requirements],
)


app = App(
    name="banking_servicing_app",
    root_agent=root_agent,
)