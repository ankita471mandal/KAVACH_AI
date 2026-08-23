from app.normalization import normalize, normalize_inverse, normalize_factors


def test_normalize_basic():
    assert normalize(150, 0, 300) == 50.0

def test_normalize_missing():
    assert normalize(None, 0, 100) is None

def test_normalize_invalid():
    assert normalize("bad", 0, 100) is None

def test_normalize_below_min_clamped():
    assert normalize(-50, 0, 100) == 0.0

def test_normalize_above_max_clamped():
    assert normalize(500, 0, 100) == 100.0

def test_normalize_degenerate_range():
    assert normalize(10, 5, 5) == 50.0

def test_normalize_inverse_low_value_high_risk():
    assert normalize_inverse(0, 0, 500) == 100.0

def test_normalize_inverse_missing():
    assert normalize_inverse(None, 0, 500) is None

def test_normalize_factors_full_set():
    raw = {
        "rainfall": 150, "river_level": 5, "elevation": 250,
        "historical_risk": 50, "drainage": 50, "trend": 0,
    }
    result = normalize_factors(raw)
    assert set(result.keys()) == {
        "rainfall", "river_level", "elevation", "historical_risk", "drainage", "trend"
    }
    assert result["elevation"] == 50.0  # midpoint, inverse of midpoint is still midpoint