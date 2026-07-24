from __future__ import annotations

import pytest

from services.ats_service import PIPELINE_STAGES


def test_pipeline_has_complete_terminal_states() -> None:
    assert "Applied" in PIPELINE_STAGES
    assert "Hired" in PIPELINE_STAGES
    assert "Rejected" in PIPELINE_STAGES
    assert len(PIPELINE_STAGES) == len(set(PIPELINE_STAGES))
