from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.tools import ToolContext


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


def set_customer_type(
    customer_type: str,
    tool_context: ToolContext,
) -> dict:
    """Set the synthetic customer's type for the current session."""

    supported_types = {"individual", "business"}
    normalized_type = customer_type.strip().lower()

    if normalized_type not in supported_types:
        return {
            "status": "unsupported_customer_type",
            "customer_type": normalized_type,
            "supported_types": sorted(supported_types),
        }

    tool_context.state["customer_type"] = normalized_type

    return {
        "status": "success",
        "customer_type": normalized_type,
    }


root_agent = Agent(
    name="banking_servicing_agent",
    model="gemini-3.6-flash",
    description="AI assistant for synthetic banking servicing workflows.",
    instruction="""
    You are an AI assistant for a synthetic banking servicing platform.

    The current session customer type is: {customer_type?}

    Your responsibilities are:
    1. Record the customer's type when the user explicitly identifies themselves
    as an individual or business customer.
    2. Answer KYC document requirement questions using the available tools.

    Rules:
    - If the user explicitly states that they are an individual or business customer,
    use the appropriate tool to store that customer type.
    - Use tools for authoritative synthetic banking information.
    - When answering from a tool result, use only facts explicitly returned by the tool.
    - Do not add examples, requirements, or policy details from your own knowledge.
    - If the user refers to their customer type and one exists in session state,
    use that value.
    - Do not invent customer information.
    - Do not claim access to real banking systems.
    - All customer and policy information in this project is synthetic.
    - If a tool cannot answer the request, say so clearly.
    """,
    tools=[
        get_kyc_requirements,
        set_customer_type,
    ],
)


app = App(
    name="banking_servicing_app",
    root_agent=root_agent,
)