import os
import pytest
from ai.severity_scoring.scorer import assess_severity

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Requires GEMINI_API_KEY")
def test_severity_p0_guardrail():
    # 'fatality' should trigger the deterministic P0 guardrail
    result = assess_severity(
        category="Accident",
        description="A major accident with a fatality occurred on the highway.",
        address="Highway 42"
    )
    assert result["priority"] == "P0"

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Requires GEMINI_API_KEY")
def test_severity_p3():
    # Simple issue should be scored low
    result = assess_severity(
        category="Garbage",
        description="Small plastic bag left on the sidewalk.",
        address="Internal colony road"
    )
    assert result["priority"] in ["P2", "P3"]
    assert "severity_score" in result
    assert "severity_reasons" in result
