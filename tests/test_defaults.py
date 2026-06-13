from editor._defaults import QUALITY, SUFFIXES, RESAMPLE


def test_quality_is_positive_int():
    assert isinstance(QUALITY, int)
    assert QUALITY > 0


def test_suffixes_has_all_operations():
    for op in ("resize", "optimize", "enhance", "pipeline"):
        assert op in SUFFIXES


def test_resample_is_known():
    assert RESAMPLE in ("LANCZOS", "BICUBIC", "BILINEAR", "NEAREST")
