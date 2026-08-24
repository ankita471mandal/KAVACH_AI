from app.classification import classify_risk


def test_classify_low():
    assert classify_risk(10) == "LOW"

def test_classify_moderate_boundary():
    assert classify_risk(31) == "MODERATE"

def test_classify_high():
    assert classify_risk(55) == "HIGH"

def test_classify_critical():
    assert classify_risk(95) == "CRITICAL"

def test_classify_none():
    assert classify_risk(None) == "UNKNOWN"

def test_classify_exact_boundary_30():
    assert classify_risk(30) == "LOW"

def test_classify_exact_boundary_71():
    assert classify_risk(71) == "CRITICAL"