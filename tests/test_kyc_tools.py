from types import SimpleNamespace

from app.agent import get_kyc_requirements, set_customer_type


def test_individual_kyc_requirements():
    result = get_kyc_requirements("individual")

    assert result["status"] == "success"
    assert result["customer_type"] == "individual"

    assert result["documents"] == [
        "government-issued photo ID",
        "proof of address",
        "tax identification document",
    ]

    assert result["data_source"] == "synthetic_demo_policy"


def test_business_kyc_requirements():
    result = get_kyc_requirements("business")

    assert result["status"] == "success"
    assert result["customer_type"] == "business"
    assert len(result["documents"]) == 4


def test_unsupported_customer_type():
    result = get_kyc_requirements("nonprofit")

    assert result["status"] == "unsupported_customer_type"
    assert result["customer_type"] == "nonprofit"
    assert result["supported_types"] == ["individual", "business"]


def test_customer_type_is_normalized():
    result = get_kyc_requirements("  INDIVIDUAL  ")

    assert result["status"] == "success"
    assert result["customer_type"] == "individual"


def test_set_customer_type_updates_state():
    tool_context = SimpleNamespace(state={})

    result = set_customer_type(
        customer_type="business",
        tool_context=tool_context,
    )

    assert result == {
        "status": "success",
        "customer_type": "business",
    }
    assert tool_context.state["customer_type"] == "business"


def test_set_customer_type_rejects_unsupported_type():
    tool_context = SimpleNamespace(state={})

    result = set_customer_type(
        customer_type="nonprofit",
        tool_context=tool_context,
    )

    assert result == {
        "status": "unsupported_customer_type",
        "customer_type": "nonprofit",
        "supported_types": ["business", "individual"],
    }
    assert "customer_type" not in tool_context.state
