import pytest
from pydantic import ValidationError

from app.api.schemas import AnalyzeRequest


def test_analyze_request_accepts_valid_text():
    request = AnalyzeRequest(
        text="Explain how DNS works."
    )

    assert request.text == "Explain how DNS works."


def test_analyze_request_rejects_empty_text():
    with pytest.raises(ValidationError):
        AnalyzeRequest(text="")

