import pytest

from app.detectors.base import Detector


def test_detector_is_abstract():
    with pytest.raises(TypeError):
        Detector()
